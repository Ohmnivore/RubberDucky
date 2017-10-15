class State:

    def __init__(self):
        self.entities = []

    def update(self, elapsed):
        for entity in self.entities:
            entity.update(elapsed)

    def render(self, elapsed, camera, program):
        for entity in self.entities:
            entity.render(elapsed, camera, program)
    
    def destroy(self):
        for entity in self.entities:
            entity.destroy()
