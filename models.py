import json


class Discs:
    def __init__(self):
        try:
            with open("discs.json", "r") as f:
                self.discs = json.load(f)
        except FileNotFoundError:
            self.discs = []

    def all(self):
        return self.discs

    def get(self, id):
        disc = [disc for disc in self.all() if disc['id'] == id]
        if disc:
            return disc[0]
        return []

    def create(self, data):
        self.discs.append(data)
        self.save_all()

    def delete(self, id):
        disc = self.get(id)
        if disc:
            self.discs.remove(disc)
            self.save_all()
            return True
        return False

    def save_all(self):
        with open("discs.json", "w") as f:
            json.dump(self.discs, f)

    def update(self, id, data):
        disc = self.get(id)
        print(disc)
        print(data)
        if disc:
            index = self.discs.index(disc)
            self.discs[index] = data
            self.save_all()
            return True
        return False
        
discs = Discs()