


class Car: #make a class called car 
    pass #classes have atrributes and method 


    def __init__ (self, make, model, year, color): # constructs objects for us 
        self.make = make 
        self.model = model #self refers to the object we are curentlu creating 
        self.color = color
        self.year = year

    def drive(self):
        print("this car is driving")
    def stop(self):
        print("this car is stopped")

car_1 = Car("ford", "mustang", "2000", "grey")

car_1.drive()
car_1.stop() # dont forget parnthesis
print(car_1.make)


class Animal:
    def __init__(self, species):
        self.species = species

class Dog(Animal):
    def __init__(self, species):
        super().__init__(species)

    def bark(self):
        print("bark")
    def describe(self):
        print(f"This is a {self.species}")

dog_1 = Dog("Golden Retriever")
print(dog_1.species)
dog_1.bark()
dog_1.describe()





class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print (f"Name: <{self.name}>, Age: <{self.age}>")

class Student(Person):
    def __init__(self, student_id, major):
        self.major = major 
        self.studentid = student_id
        
