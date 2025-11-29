class Ship:
    def __init__(self):
        self.__fuel = 100
        self.__hull_integrity = 100
        self.__oxygen = 100
        self.__spare_parts = 100,
        self.__food = 100,
        self.__water = 100,
        self.__medical = 100,
        self.__ammo = 100

    def get_fuel (self):
        return str(self.__fuel) + "%"

    def set_fuel (self, fuel):
        self.__fuel = fuel

    def get_hull_integrity (self):
        return str(self.__hull_integrity) + "%"

    def set_hull_integrity (self, hull_integrity):
        self.__hull_integrity = hull_integrity

    def get_oxygen (self):
        return self.__oxygen

    def set_oxygen (self, oxygen):
        self.__oxygen = oxygen

    def get_spare_parts (self):
        return str(self.__spare_parts) + "%"

    def set_spare_parts (self, spare_parts):
        self.__spare_parts = spare_parts

    def get_food (self):
        return str(self.__food) + "%"

    def set_food (self, food):
        self.__food = food

    def get_water (self):
        return str(self.__water) + "%"

    def set_water (self, water):
        self.__water = water

    def get_medical (self):
        return str(self.__medical) + "%"

    def set_medical (self, medical):
        self.__medical = medical

    def get_ammo (self):
        return str(self.__ammo) + "%"

    def set_ammo (self, ammo):
        self.__ammo = ammo