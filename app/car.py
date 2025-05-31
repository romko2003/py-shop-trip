import dataclasses


@dataclasses.dataclass
class Car:
    fuel_consumption_per_100km: float

    def calculate_fuel_liters_for_distance(self, distance_km: float) -> float:
        """
        Розраховує кількість літрів палива, необхідних для заданої відстані.
        """
        if distance_km < 0:  # Запобігаємо від'ємній відстані
            distance_km = 0
        return (distance_km / 100.0) * self.fuel_consumption_per_100km_consumption_per_100km
