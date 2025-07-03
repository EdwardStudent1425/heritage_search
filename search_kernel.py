from adapters.martyrology import MartyrologyAdapter
from adapters.openlist import OpenlistAdapter
from adapters.reabit import ReabitAdapter

class SearchKernel:

    def __init__(self):
        self.parsers = [
            OpenlistAdapter(),
            MartyrologyAdapter()
            # ReabitAdapter(),
            # HolodomorVictimsAdapter
        ]
    
    def search_all(self, query: dict, available_sites):
        result = []
        for link in available_sites:
            for parser in self.parsers:
                if link == parser.url:
                    result.append(parser.search(query))

        return result
