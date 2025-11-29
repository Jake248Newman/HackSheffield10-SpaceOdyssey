class Ship:
    def __init__(self):
        self.__fuel = 100
        self.__hull_integrity = 100
        self.__speed = 0.0
        self.__oxygen = 100
        self.__supplies = {
            "Spare parts" : 100,
            "Food": 100,
            "Water": 100,
            "Medical": 100,
            "Ammo": 100
        }

    def get_fuel (self):
        return self.__fuel

    def get_hull_integrity (self):
        return self.__hull_integrity

    def get_speed (self):
        return self.__speed

    def get_oxygen (self):
        return self.__oxygen

    def set_fuel (self, fuel):
        self.__fuel = fuel

    def set_hull_integrity (self, hull_integrity):
        self.__hull_integrity = hull_integrity

    def set_speed (self, speed):
        self.__speed = speed

    def set_oxygen (self, oxygen):
        self.__oxygen = oxygen

    def get_supplies (self):
        return (
            "Spare parts: " + str(self.__supplies["Spare parts"]) + "% " +
            "Food: " + str(self.__supplies["Food"]) + "% " +
            "Water: " + str(self.__supplies["Water"]) + "% " +
            "Medical: " + str(self.__supplies["Medical"]) + "% " +
            "Ammo: " + str(self.__supplies["Ammo"]) + "%"
        )

    def to_dict(self):
        return {
            'fuel': self.__fuel,
            'hull_integrity': self.__hull_integrity,
            'speed': self.__speed,
            'oxygen': self.__oxygen
        }