from yaml import safe_load as yaml_load, safe_dump as yaml_dump
from json import loads as json_load, dumps as json_dump, load as json_load_file, dump as json_dump_file
from .ortreg.listearten import listearten
from .address_system import Ort, Blick
from pathlib import Path
from filelock import FileLock
import appdirs
from sqlite3 import connect
from .ortreg.finding import finDing
from weakref import ref, WeakValueDictionary
from .kind_classes.kind_tree import artvon
from .ortreg.setzding import setzDing
from .ortreg.ansicht import ansicht
from .ortreg.machding import machDing
from .ortreg.thing import Thing
from .kind_classes.kind import _Kind, _register_hardcoded_kind_classes
from .kind_classes.ownership_tree import OwnershipTree, istFrei
from .kind_classes.kind_tree import _KindTree, root_tree_address
from .kind_classes.unbek import Unbek
from .kind_classes.gpgpub import _GpgPub
from .kind_classes.gpgpriv import _GpgPriv
from .kind_classes.identity import _Identity
from .kind_classes.text import _Text
from .kind_classes.ortlink import _OrtLink
from typing import Self, Callable
from .ortreg.data_formats import json_format, raw_format

_hardcoded_kind_classes = [_Kind, OwnershipTree, _KindTree, _GpgPub, _GpgPriv, _Identity, _Text, _OrtLink]
_register_hardcoded_kind_classes(_hardcoded_kind_classes)

class Database:
    def __init__(self, folder = None, seed = None):
        # Set database settings
        self._prefered_data_format = json_format
        # Load general information
        static_data_path = Path(__file__).parent / "static_data"
        general_info_path = static_data_path / "general_info.yaml"
        with general_info_path.open("r") as f:
            general_info = yaml_load(f)
        data_pool_name = general_info["data_pool"]
        version = general_info["version"]
        # Find the data pool folder
        if folder == None:
            folder = Path(appdirs.user_data_dir("distrida")) / data_pool_name
        else:
            folder = Path(folder)
        folder.mkdir(parents = True, exist_ok = True)
        # Lock the data pool folder
        lock_path = folder / "lock"
        self._lock = FileLock(str(lock_path))
        self._lock.acquire()
        if not self._lock.is_locked:
            raise RuntimeError("Could not lock the data pool folder")
        # Check the data pool version
        data_pool_general_info_path = folder / "general_info.yaml"
        if data_pool_general_info_path.exists():
            with data_pool_general_info_path.open("r") as f:
                old_version = yaml_load(f)["version"]
        else:
            old_version = None
        with data_pool_general_info_path.open("w") as f:
            yaml_dump(general_info, f)
        # Create the database connection
        database_path = folder / "database.sqlite"
        database_new = not database_path.exists()
        self._db = connect(str(database_path))
        if database_new:
            # Load json seed
            if seed == None:
                seed_path = static_data_path / "distrida_database_seed.json"
                seed = json_load_file(seed_path.open("r"))
            # Create the database schema
            self._db.execute("CREATE TABLE things (id BLOB PRIMARY KEY, raw BLOB, json TEXT)")
            # Insert the seed data
            for kind_identifyer, thing_dict in seed.items():
                for thing_identifyer, thing in thing_dict.items():
                    self._db.execute("INSERT INTO things (id, raw, json) VALUES (?, ?, ?)", (bytes(Ort(thing_identifyer)), None, json_dump(thing, sort_keys=True)))
            self._db.commit()
        # Prepare WeakValueDictionary for things
        self._things = WeakValueDictionary()
        # Load hardcoded kinds
        self._hardcoded_kinds = set()
        for kind_class in _hardcoded_kind_classes:
            self._hardcoded_kinds.add(self._get_thing_from_function(kind_class.kind_address, _Kind))
        # Load root kind tree
        self._root_kind_tree = self._get_thing_from_function(root_tree_address, _KindTree)
        #listearten(self)
    def _register_thing(self, thing: _Kind):
        '''
        Registers a thing
        '''
        self._things[thing.address] = thing
    def _unregister_thing(self, thing: _Kind):
        '''
        Unregisters a thing
        '''
        del self._things[thing.address]
    def get_thing(self, ort: Ort) -> _Kind:
        '''
        Returns the thing with the given Ort
        '''
        # Return thing if it is already loaded
        if ort in self._things:
            return self._things[ort]
        # Get the kind of the thing
        kind_address, kind_address_asighner = self._root_kind_tree.interface(Ort("Ssb")).find_address_kind_information(ort)
        if kind_address == None:
            raise RuntimeError("Thing not found")
        # Load the thing
        return self._get_thing_from_kind_address(ort, kind_address)
    def _get_thing_from_kind_address(self, address: Ort, kind_address: Ort) -> _Kind:
        '''
        Loads a thing manually using the given kind address
        '''
        # Return thing if it is already loaded
        if address in self._things:
            return self._things[address]
        # Load kind
        kind = self.get_thing(kind_address)
        # Load thing from database
        return kind.interface(Ort("Ssa")).get_thing(address)
    def _get_thing_from_function(self, address: Ort, thing_creator: Callable[[any, bytes, Ort, Self], Thing]) -> _Kind:
        '''
        Loads a thing manually using the given thing creator function
        '''
        # Return thing if it is already loaded
        if address in self._things:
            return self._things[address]
        # Load thing from database
        return thing_creator(*self._get_database_entry(address), address, self)
    def _get_database_entry(self, ort: Ort) -> tuple[str | bytes, bytes]:
        '''
        Returns the data pool entry for a given Ort
        The return value is a tuple of the data and the format of the data encoded as bytes (b'json' or b'raw')
        '''
        c = self._db.cursor()
        c.execute("SELECT raw, json FROM things WHERE id = ?", (bytes(ort),))
        raw, json = c.fetchone()
        c.close()
        if raw != None:
            return (raw, b"raw")
        elif json != None:
            return (json_load(json), json_format)
        else:
            raise RuntimeError("Database entry not found")
    def _set_database_entry(self, ort: Ort, data: bytes, format: bytes):
        '''
        Sets the data pool entry for a given Ort
        The format of the data is encoded as bytes (b'json' or b'raw')
        '''
        c = self._db.cursor()
        if format == raw_format:
            c.execute("UPDATE things SET raw = ?, json = NULL WHERE id = ?", (data, bytes(ort)))
        elif format == json_format:
            c.execute("UPDATE things SET raw = NULL, json = ? WHERE id = ?", (json_dump(data, sort_keys=True), bytes(ort)))
        else:
            raise RuntimeError("Unknown data format")
        c.close()
    def _update_thing_data(self, thing: Thing, data: any, format: bytes):
        '''
        Updates the data of a thing
        The format of the data is encoded as bytes (b'json' or b'raw')
        '''
        if format != self._prefered_data_format:
            data = thing._kind._convert_data_format(data, format, self._prefered_data_format)
        self._set_database_entry(thing.address, data, self._prefered_data_format)



    def __del__(self):
        self._db.close()
        self._lock.release()
    def speicher(self, pfad = None):
        if pfad == None:
            self._f.seek(0)
            yaml_dump(self._reg, self._f)
        else:
            with open(pfad, "w") as f:
                yaml_dump(self._reg, f)
    def listOrts(self, arts):
        r = self._reg.get(arts)
        return [*r.keys()] if r else []
    def ladeJSON(self, arts, orts):
        r = self._reg.get(arts)
        return r.get(orts) if r else None
    def setzeJSON(self, arts, orts, daten):
        r = self._reg.get(arts)
        if not r:
            r = {}
            self._reg[arts] = r
        r[orts] = daten
    def __call__(self):
        return self
    def __getitem__(self, address : Ort) -> _Kind:
        return self.get_thing(address)
    def __setitem__(self, orts, address):
        if not type(item) is tuple:
            item = (item,)
        self.setz(orts, item)

    
    def find(self, orts):
        return finDing(orts, ref(self))
    def artvon(self, orts):
        return artvon(orts, ref(self))
    def setz(self, orts, inh):
        return setzDing(orts, inh, ref(self))
    def ansicht(self):
        return ansicht(ref(self))
    def mach(self, art, args):
        return machDing(art, args, ref(self))
    def frei(self, orts):
        return istFrei(orts, ref(self))
