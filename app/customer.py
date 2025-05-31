import dataclasses
from typing import List, Dict, TYPE_CHECKING

# Для уникнення циклічного імпорту, якщо Car знаходиться в іншому файлі
if TYPE_CHECKING:
    from .car import Car


@dataclasses.dataclass
class Customer:
    name: str
    product_cart: Dict[str, int] # Назва товару: кількість
    current_location: List[float] # Поточне місцезнаходження клієнта, яке може змінюватися
    money: float
    car: 'Car' # Екземпляр класу Car

    # Зберігаємо початкове місцезнаходження для розрахунку поїздки додому
    initial_location: List[float] = dataclasses.field(init=False)

    def __post_init__(self):
        # Копіюємо початкове місцезнаходження, щоб воно не змінювалося, коли оновлюється current_location
        self.initial_location = list(self.current_location)