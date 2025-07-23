from dataclasses import dataclass

@dataclass
class Predictions():
    confidence: float
    violation: str
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
 