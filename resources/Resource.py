from abc import abstractmethod, ABC


class Resource(ABC):
    @abstractmethod
    def type(self) -> str:
        pass

    def params(self) -> dict:
        return {}

    @abstractmethod
    def to_dict(self) -> dict:
        pass
