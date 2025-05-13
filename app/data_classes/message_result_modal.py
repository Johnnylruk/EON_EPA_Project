from dataclasses import dataclass

@dataclass
class Predictions():
    confidence: int
    violation: str
    violation_id: int
    detection_id: int

@dataclass
class MessageResult():
    violations: list[Predictions]
    output_image : str
 