class CrewMember:
    def __init__(self, name, job):
        self.name = name
        self.health = 100
        self.sanity = 100
        self.status = "Alive"
        self.hunger = 100
        self.job = job

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_health(self):
        return str(self.health) + "%"

    def set_health(self, health):
        self.health = health

    def get_sanity(self):
        return str(self.sanity) + "%"

    def set_sanity(self, sanity):
        self.sanity = sanity

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_hunger(self):
        return str(self.hunger) + "%"

    def set_hunger(self, hunger):
        self.hunger = hunger

    def get_job(self):
        return self.job

    def set_job(self, job):
        self.job = job

    #todo update this
    def to_dict(self):
        return {
            "name": self.name,
            "occupation": self.job,
            "health": self.health
        }