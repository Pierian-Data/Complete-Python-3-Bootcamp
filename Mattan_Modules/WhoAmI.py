import random
class Mattan ():

    birth_date = '1993-10-11'
    birth_name = 'Mattan Joshua Romano'

    def __init__ (self):
        print("An instance of object Mattan has been created.")

    def pick_number (self,lower:int, upper:int) -> int: 
        return random.randint(1,100)

    def __str__ (self)-> str:
        return Mattan.birth_name

    def __len__ (self) -> int:
        return len(Mattan.birth_name)
