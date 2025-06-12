from dataclasses import dataclass

# Services Model
@dataclass
class ViolationLogs():
    violation: str
    date: str
    time: str
    description: str

# Routing Model
@dataclass
class ViolationMessage():
    message: ViolationLogs