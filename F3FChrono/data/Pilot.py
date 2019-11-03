

class Pilot:

    def __init__(self, name, first_name, f3x_vault_id=None, fai_id=None, national_id=None):
        self._name = name
        self._first_name = first_name
        self._fai_id = fai_id
        self._national_ID = national_id
        self._f3x_vault_id = f3x_vault_id

    def get_f3x_vault_id(self):
        return self._f3x_vault_id

    def to_string(self):
        return self._name + '\t' + self._first_name
