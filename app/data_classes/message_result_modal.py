from dataclasses import dataclass

@dataclass
class Prediction():
    x1: float
    y1: str
    x2: int
    y2: int
    confidence: float
    violation: float 

@dataclass 
class Person():
    person: Prediction
    violations: list

@dataclass
class MessageResult():
    person_detected: list[Person]
 