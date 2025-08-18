class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname
        print("person init")
    
    def printname(self):
        print(self.firstname, self.lastname)

class Student(Person):
  def __init__(self, fname, lname, year):
      super().__init__(fname, lname)
      self.graduationyear = year
      print("Student init")

  def welcome(self):
      
      super().printname()
      print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

# x = Student("Ankush", "Rathi", 2019)
# x.welcome()

y = Person("Aditi", "Tiwari")
y.printname()
