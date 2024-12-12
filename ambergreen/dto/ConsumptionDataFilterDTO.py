class ConsumptionDataFilterDTO:
    def __init__(self, institution_id):
        self.__institution_id = institution_id

    def get_institution_id(self):
        return self.__institution_id
