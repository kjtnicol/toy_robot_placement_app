from abc import ABC, abstractmethod


class ToyRobotPlacementInterface(ABC):
    @abstractmethod
    def apply_command(self, command: str, *args):
        pass
