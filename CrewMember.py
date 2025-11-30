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
        return self.health

    def set_health(self, health):
        self.health = health

    def get_sanity(self):
        return self.sanity

    def set_sanity(self, sanity):
        self.sanity = sanity

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_hunger(self):
        return self.hunger

    def set_hunger(self, hunger):
        self.hunger = hunger

    def decrease_hunger(self, num):
        self.hunger = self.hunger - num

    def get_job(self):
        return self.job

    def set_job(self, job):
        self.job = job

    def get_crew_context(self):
        """Returns a formatted personnel string for the AI"""
        return f"""
        [PERSONNEL FILE: {self.name.upper()}]
        Role: {self.job}
        Status: {self.status}

        [BIOMETRICS]
        - Health: {self.health}%
        - Hunger: {self.hunger}% (Lower is hungry)
        - Mental Stability: {self.sanity}%
        """