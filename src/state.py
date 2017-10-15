class State:

    def __init__(self):
        self.entities = []

    def update(self):
        for entity in self.entities:
            entity.update()

    def render(self, camera, program):
        for entity in self.entities:
            entity.render(camera, program)
    
    def destroy(self):
        for entity in self.entities:
            entity.destroy()
