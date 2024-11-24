from sharedInfrastructure.abstractRepository import AbstractRepository


class InMemoryRepository(AbstractRepository):

    def __init__(self):
        self.data = {}

    def add(self, chocolate_box):
        self.data[chocolate_box.id] = chocolate_box

    def get(self, id):
        return self.data.get(id)

    def remove(self, chocolate_box):
        del self.data[chocolate_box.id]