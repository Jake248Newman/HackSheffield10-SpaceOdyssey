class CrewMember:
    def __init__(self, name, age, gender, occupation):
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.health = 100

    def get_name(self):
        return self.name
    def get_age(self):
        return self.age
    def get_gender(self):
        return self.gender
    def get_occupation(self):
        return self.occupation
    def get_health(self):
        return self.health
    def set_health(self, health):
        self.health = health
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "occupation": self.occupation,
            "health": self.health
        }
