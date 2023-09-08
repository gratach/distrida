from ..address_system import Ort, Blick
from ..database import Database, _hardcoded_kind_classes
from ..kind_classes.kind import _Kind
from ..kind_classes.kind_tree import _KindTree, root_tree_address
from tempfile import TemporaryDirectory
from json import loads
def create_minimal_database_seed():
    kinds = {str(kind.kind_address) : {} for kind in _hardcoded_kind_classes}
    seed = {
        str(_Kind.kind_address) : kinds,
        str(_KindTree.kind_address) : {
            str(root_tree_address) : {}
        }
    }
def create_database_seed():
    with TemporaryDirectory() as tempdir:
        minimal_seed = create_minimal_database_seed()
        db = Database(tempdir, seed=minimal_seed)
    