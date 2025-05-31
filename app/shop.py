import dataclasses
from typing import List, Dict


@dataclasses.dataclass
class Shop:
    name: str
    location: List[float] # Місцезнаходження магазину
    products: Dict[str, float] # Назва товару: ціна