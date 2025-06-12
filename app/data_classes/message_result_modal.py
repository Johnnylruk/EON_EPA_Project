from dataclasses import dataclass

@dataclass
class Predictions():
    confidence: int
    violation: str
    violation_id: int
    detection_id: int
    width: int
    height: int
    x: float
    y: float 

@dataclass 
class Person():
    person: Predictions
    violations: list

@dataclass
class MessageResult():
    person_detected: list[Person]
 