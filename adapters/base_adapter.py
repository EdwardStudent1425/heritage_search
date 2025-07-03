from abc import ABC, abstractmethod

class ArchiveAdapter(ABC):
    '''
    ArchiveAdapter class
    '''
    @abstractmethod
    def search(self, query: str) -> list:
        """
        an abstract method for the search fucntion
        """
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass
