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
class MessageResult():
    helmet_violation: Helmet
    hi_vis_violation: HiVis
    output_image : str
 