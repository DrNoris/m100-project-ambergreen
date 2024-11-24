class Entity:
    def __init__(self, entity_id = None):
        self.__id = entity_id

    def getId(self):
        return self.__id

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.__id})"

    def __eq__(self, other):
        return self.__id == other.__id