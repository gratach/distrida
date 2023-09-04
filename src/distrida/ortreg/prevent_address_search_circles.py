from ..address_system import Ort, Blick

# This is a dictionary that contains for all destination addresses a tuple of:
# - the distance to the current address cone.
# - the number of search iterations that are currently running for this destination address.
_current_address_searches = {}
class PreventAddressSearchCircles:
    def __init__(self, destination_address : Ort, current_address_cone : Blick, strict : bool = False):
        """
        This class is used to prevent address search circles.
        It can be used as a context manager that returns the relative address of the destination address.
        It will raise an exception if the distance between the current address cone and the destination address is larger than it was for a previous, but still running search for the same destination address.
        """
        self._destination_address = destination_address
        self._relative_address = current_address_cone.aufOrt(destination_address)
        self._search_distance = len(self._relative_address.weg)
        self._strict = strict
    def __enter__(self):
        global _current_address_searches
        current_address_search = _current_address_searches.get(self._destination_address)
        if current_address_search != None and (current_address_search[0] <= self._search_distance if self._strict else current_address_search[0] < self._search_distance):
            raise Exception("Address search circle detected")
        _current_address_searches[self._destination_address] = (self._search_distance, current_address_search[1] + 1 if current_address_search != None else 1)
        return self._relative_address
    def __exit__(self, exc_type, exc_value, traceback):
        global _current_address_searches
        current_address_search = _current_address_searches.get(self._destination_address)
        assert current_address_search != None
        if current_address_search[1] == 1:
            del _current_address_searches[self._destination_address]
        else:
            _current_address_searches[self._destination_address] = (current_address_search[0], current_address_search[1] - 1)