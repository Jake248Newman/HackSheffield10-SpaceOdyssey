class Ship:
    def __init__(self):
        self.__fuel = 100
        self.__hull_integrity = 100
        self.__oxygen = 100
        self.__spare_parts = 100
        self.__food = 100
        self.__water = 100
        self.__medical = 100
        self.__ammo = 100
        self.__year = 3025
        self.__month = 2
        self.__day = 5
        self.__days = 1

    def get_days(self):
        return self.__days

    def get_date(self):
        return str(self.__day) + "/" + str(self.__month) + "/" + str(self.__year)

    def increase_date(self):
        self.__days += 1

        self.__day += 1

        if self.__day == 31:
            self.__day = 1
            self.__month += 1

        if self.__month == 13:
            self.__month = 1
            self.__year += 1

    def get_fuel (self):
        return self.__fuel

    def set_fuel (self, fuel):
        self.__fuel = fuel

    def decrease_fuel(self):
        self.__fuel -= 1

    def get_hull_integrity (self):
        return self.__hull_integrity

    def set_hull_integrity (self, hull_integrity):
        self.__hull_integrity = hull_integrity

    def get_oxygen (self):
        return self.__oxygen

    def set_oxygen (self, oxygen):
        self.__oxygen = oxygen

    def get_spare_parts (self):
        return self.__spare_parts

    def set_spare_parts (self, spare_parts):
        self.__spare_parts = spare_parts

    def get_food (self):
        return self.__food

    def set_food (self, food):
        self.__food = food

    def decrease_food(self, num):
        self.__food -= num

    def get_water (self):
        return self.__water

    def set_water (self, water):
        self.__water = water

    def get_medical (self):
        return self.__medical

    def set_medical (self, medical):
        self.__medical = medical

    def get_ammo (self):
        return self.__ammo

    def set_ammo (self, ammo):
        self.__ammo = ammo

    def get_ai_context(self):
        """Returns a formatted string for the AI prompt"""
        return f"""
        [SHIP STATUS REPORT]
        Current Date: {self.__year}-{self.__month:02d}-{self.__day:02d}
        Mission Day: {self.__days}

        [VITAL SYSTEMS]
        - Fuel: {self.__fuel}%
        - Hull Integrity: {self.__hull_integrity}%
        - Oxygen Levels: {self.__oxygen}%

        [CARGO MANIFEST]
        - Food Reserves: {self.__food}%
        - Water Reserves: {self.__water}%
        - Medical Supplies: {self.__medical}%
        - Spare Parts: {self.__spare_parts}
        - Ammunition: {self.__ammo}
        """