from dataclasses import dataclass


@dataclass(frozen=True)
class ManagerChoices:
    DEFAULT = "default"
    CUSTOM = "custom"
