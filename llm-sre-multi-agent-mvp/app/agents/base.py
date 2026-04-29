from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
