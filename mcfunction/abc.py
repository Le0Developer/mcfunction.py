
import abc


class Node(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError


class ParsedCommand(metaclass=abc.ABCMeta):
    command: str

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError
