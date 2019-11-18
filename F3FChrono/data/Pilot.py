

class Pilot:

    def __init__(self, name, first_name, pilot_id=None, f3x_vault_id=None, fai_id=None, national_id=None):
        self.id = pilot_id
        self.name = name
        self.first_name = first_name
        self.fai_id = fai_id
        self.national_ID = national_id
        self.f3x_vault_id = f3x_vault_id

    def get_f3x_vault_id(self):
        return self.f3x_vault_id

    def to_string(self):
        return self.name + '\t' + self.first_name
