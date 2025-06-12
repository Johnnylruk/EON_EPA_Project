from dataclasses import dataclass

@dataclass
class ViolationLogs():
    violation: str
    date: str
    time: str
    description: str
