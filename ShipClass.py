class Ship:
    def __init__(self):
        self.fuel = 100
        self.hull_integrity = 100
        self.speed = 0.0
        self.oxygen = 100
        self.supplies = {"Spare parts" : 100, "Food": 100, "Water": 100, "Medical": 100, "Ammo": 100}

    def get_fuel (self):
        return self.fuel
    def get_hull_integrity (self):
        return self.hull_integrity
    def get_speed (self):
        return self.speed
    def get_oxygen (self):
        return self.oxygen
    def set_fuel (self, fuel):
        self.fuel = fuel
    def set_hull_integrity (self, hull_integrity):
        self.hull_integrity = hull_integrity
    def set_speed (self, speed):
        self.speed = speed
    def set_oxygen (self, oxygen):
        self.oxygen = oxygen
    def to_dict(self):
        return {
            'fuel': self.fuel,
            'hull_integrity': self.hull_integrity,
            'speed': self.speed,
            'oxygen': self.oxygen
        }
