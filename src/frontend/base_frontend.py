from abc import ABC, abstractmethod


class BaseFrontend(ABC):
    @abstractmethod
    def run(self) -> None:
        ...
