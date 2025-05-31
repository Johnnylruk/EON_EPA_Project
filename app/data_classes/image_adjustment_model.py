from dataclasses import dataclass
from numpy.typing import NDArray
from cv2.dnn import Net
@dataclass
class ImageAdjustmentModel():
    prototxt_path: str
    model_path: str
    width: int
    height: int
    kernel_width: int
    kernel_height: int
    image_file: NDArray
    model: Net
    output: NDArray
