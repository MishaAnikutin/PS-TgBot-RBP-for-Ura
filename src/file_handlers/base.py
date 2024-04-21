from abc import ABC, abstractproperty, abstractmethod


class BaseFile(ABC):
    @abstractproperty
    def bytes(self):
        ...
        
    @abstractmethod
    def get_number_pages(self):
        ...


class BasePhoto(ABC):
    @abstractproperty
    def bytes(self):
        ...
        
    @abstractmethod
    def get_number_pages(self):
        ...

    