from ..kind_classes.ident import meineIdents
def binIch(idorts, weak):
    return idorts in [x._orts for x in meineIdents(weak)]
