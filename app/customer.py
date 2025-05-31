import dataclasses
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .car import Car

@dataclasses.dataclass
class Customer:
    name: str
    product_cart: Dict[str, int]
    current_location: List[float]
    money: float
    car: 'Car'

    initial_location: List[float] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
              self.initial_location = list(self.current_location)
