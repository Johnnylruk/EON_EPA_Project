from dataclasses import dataclass

@dataclass
class Predictions():
    confidence: int
    violation: str
    violation_id: int
    detection_id: int  

@dataclass 
class Helmet():
    violations: list[Predictions]
    amount: int

@dataclass 
class HiVis():
    violations: list[Predictions]
    amount: int

@dataclass
class Object_Violations():
    helmet_violation: list[Helmet]
    hi_vis_violation: list[HiVis]

@dataclass
class Violation_Types():
    helmet: Helmet
    hi_vis: HiVis

@dataclass 
class Person():
    violations: Object_Violations


@dataclass
class MessageResult():
    person_detected: Person
    output_image : str
 