from yaml import safe_load as yaml_load, safe_dump as yaml_dump
from json import loads as json_load, dumps as json_dump
from .ortreg.listearten import listearten
from .address_system import Ort, Blick
from pathlib import Path
from filelock import FileLock
import appdirs
from sqlite3 import connect
from .ortreg.finding import finDing
from weakref import ref
from .kind_classes.artbaum import artvon
from .ortreg.setzding import setzDing
from .ortreg.ansicht import ansicht
from .ortreg.machding import machDing
from .kind_classes.kind import _Kind 
from .kind_classes.habebaum import _HabeBaum, istFrei
from .kind_classes.artbaum import _ArtBaum 
from .kind_classes.unbek import Unbek
from .kind_classes.gpgpub import _GpgPub
from .kind_classes.gpgpriv import _GpgPriv
from .kind_classes.ident import _Ident
from .kind_classes.text import _Text
from .kind_classes.ortlink import _OrtLink
class Database:
    def __init__(self, folder = None):
        # Load general information
        static_data_path = Path(__file__).parent / "static_data"
        general_info_path = static_data_path / "general_info.yaml"
        with general_info_path.open("r") as f:
            general_info = yaml_load(f)
        data_pool_name = general_info["data_pool"]
        version = general_info["version"]
        seed_path = static_data_path / "distrida_database_seed.yaml"
        with seed_path.open("r") as f:
            self._reg = yaml_load(f)
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
            # Create the database schema
            self._db.execute("CREATE TABLE things (id BLOB PRIMARY KEY, raw BLOB, json TEXT)")
            # Insert the seed data
            for kind_identifyer, thing_dict in self._reg.items():
                for thing_identifyer, thing in thing_dict.items():
                    self._db.execute("INSERT INTO things (id, raw, json) VALUES (?, ?, ?)", (bytes(Ort(thing_identifyer)), None, json_dump(thing, sort_keys=True)))
            self._db.commit()
        # Load kind classes
        for kind_class in [_Kind, _HabeBaum, _ArtBaum, _GpgPub, _GpgPriv, _Ident, _Text, _OrtLink]:
            pass
        listearten(self)
    def _get_database_entry(self, orts: Ort) -> tuple[str | bytes, bytes]:
        '''
        Returns the data pool entry for a given Ort
        The return value is a tuple of the data and the format of the data encoded as bytes (b'json' or b'raw')
        '''
        orts = Ort(orts)
        c = self._db.cursor()
        c.execute("SELECT raw, json FROM things WHERE id = ?", (bytes(orts),))
        raw, json = c.fetchone()
        c.close()
        if raw != None:
            return (raw, b"raw")
        elif json != None:
            return (json, b"json")
        else:
            raise RuntimeError("Database entry not found")
    def _set_database_entry(self, orts: Ort, data: bytes, format: bytes):
        '''
        Sets the data pool entry for a given Ort
        The format of the data is encoded as bytes (b'json' or b'raw')
        '''
        orts = Ort(orts)
        c = self._db.cursor()
        if format == b"raw":
            c.execute("UPDATE things SET raw = ?, json = NULL WHERE id = ?", (data, bytes(orts)))
        elif format == b"json":
            c.execute("UPDATE things SET raw = NULL, json = ? WHERE id = ?", (data, bytes(orts)))
        else:
            raise RuntimeError("Unknown data format")
        c.close()
        
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
    def __getitem__(self, item):
        return self.find(item)
    def __setitem__(self, orts, item):
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
