class Pet:
    def __init__(self, name):
        self.name = name 
    
    def __str__(self) -> str:
        return self.name


hamster = Pet(name="Fluffi")
print(hamster)