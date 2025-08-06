# Zoo Management System

from abc import ABC, abstractmethod


class Zoo():
    def __init__(self, name, location):
        self.__name     = name
        self.__location = location
        self.__enclosures = []
        self.__employees  = []

    def __str__(self):
        zoo_name = f"{self.__name} Zoo"
        zoo_name_len = len(zoo_name) + 1

        output = []
        output.append("\n" + zoo_name)
        output.append("=" * zoo_name_len)
        output.append(f"Name       : {self.__name}")
        output.append(f"Location   : {self.__location}\n")
        output.append(f"Enclosures : {len(self.__enclosures)}")
        
        if self.__enclosures:
            enclosure_ids = [str(e.getEnclosureId()) for e in self.__enclosures]
            output.append(f"  -> IDs   : {', '.join(enclosure_ids)}\n")
        else:
            output.append("  -> No enclosures added.")

        output.append(f"Employees  : {len(self.__employees)}")
        

        if self.__employees:
            for emp in self.__employees:
                role = emp.__class__.__name__
                output.append(f"  - {emp.getName()} ({role})")

        else:
            output.append("  -> No employees added.\n")

        finalString = "\n".join(output) + "\n"
        return finalString
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    def getLocation(self):
        return self.__location
    
    def getEnclosures(self):
        for e in self.__enclosures:
            print(e.enclosureId)

    def getEmployees(self):
        for e in self.__employees:
            print(e.employeesId)

    def addEnclosureToZoo(self, enclosure):
        self.__enclosures.append(enclosure)

    def addEmployeeToZoo(self, employee):
        self.__employees.append(employee)


class Enclosure():
    __enclosureIdCount = 0

    def __init__(self, capacity, zoo):
        self.__enclosureId           = 'E' + str(Enclosure.__enclosureIdCount)
        Enclosure.__enclosureIdCount = Enclosure.__enclosureIdCount + 1

        self.__capacity = capacity
        self.__zoo      = zoo
        self.__animals  = []

        zoo.addEnclosureToZoo(self)

    def __add__(self, animal):
        self.__animals.append(animal)
        animal.addToEnclosure(self)

    def __len__(self):
        return len(self.__animals)
    
    def __iter__(self):
        return iter(self.__animals) 

    def addAnimal(self, animal):
        self.__add__(animal)

    def removeAnimal(self, animal):
        self.__animals.remove(animal)

    def getEnclosureId(self):
        return self.__enclosureId
    
    def getCapacity(self):
        return self.__capacity
    
    def getZoo(self):
        return self.__zoo.getName()
    
    def getAnimals(self):
        if self.__animals:
            for a in self.__animals:
                print(a.getName())
        else:
                print('No Animals In the Enclosure')


class Employee(ABC):
    __employeeIdCount = 0

    def __init__(self, name, zoo):
        self.__employeeId          = 'EMP' + str(Employee.__employeeIdCount)
        Employee.__employeeIdCount = Employee.__employeeIdCount + 1
        
        self.__name = name
        self.__zoo = zoo

        zoo.addEmployeeToZoo(self)


    def getId(self):
        return self.__employeeId

    def getName(self):
        return self.__name
    
    def getRole(self):
        return self.__role

    def getZoo(self):
        return self.__zoo.getName()
    

class Veterinarian(Employee):
    def __init__(self, name, zoo, licensed):
        super().__init__(name,zoo)

        self.__licensed = licensed
    
    def treatAnimal(self, animal):
        if animal.getHealth() < 100:
            print('Treating the animal ..')
            animal.setHealth(animal.getHealth() + 10)

            if animal.getHealth() > 100:
               animal.setHealth(100)
        else:
            print('Animal is already healthy')
    
    def getLicenseStatus(self):
        return self.__licensed


class Zookeeper(Employee):
    def __init__(self, name, zoo, shift):
        super().__init__(name, zoo)

        self.__shift = shift

    def feedAnimal(self, animal):
        animal.feed()

    def moveAnimalToEnclosure(self, animal, enclosure):
        if animal.getEnclosure() != 'The animal is not yet in an enclosure.':
            animal.getEnclosure().removeAnimal(animal)
        enclosure + animal

    def getShift(self):
        return self.__shift


class Animal(ABC):
    def __init__(self, name, age, health):
        self.__name      = name
        self.__age       = age
        self.__health    = health
        self.__enclosure = 'None'
    
    @classmethod
    @abstractmethod
    def fromBirth(cls, name):
        pass

    @abstractmethod
    def makeSound(self):
        pass

    @abstractmethod
    def feed(self):
        pass

    def addToEnclosure(self, enclosure):
        self.__enclosure = enclosure

    def getName(self):
        return self.__name
    
    def getAge(self):
        return self.__age
    
    def getHealth(self):
        return self.__health
    
    def setHealth(self, health):
        self.__health = health
    
    def getEnclosure(self):
        if self.__enclosure == 'None':
            return 'The animal is not yet in an enclosure.'
        else:
            return self.__enclosure


class Mammal(Animal, ABC):
    def __init__(self, name, age, health, hasFur):
        Animal.__init__(self, name, age, health)

        self.__hasFur = hasFur

    def getFurStatus(self):
        return self.__hasFur
    

class Bird(Animal, ABC):
    def __init__(self, name, age, health, canFly):
        Animal.__init__(self, name, age, health)

        self.__canFly = canFly

    def getFlyingAbility(self):
        return self.__canFly


class Fish(Animal, ABC):
    def __init__(self, name, age, health, waterType):
        Animal.__init__(self, name, age, health)

        self.__waterType = waterType

    def getWaterType(self):
        return self.__waterType


class Reptile(Animal, ABC):
    def __init__(self, name, age, health, skinType):
        Animal.__init__(self, name, age, health)

        self.__skinType = skinType

    def getSkinType(self):
        return self.__skinType


class Lion(Mammal):
    def __init__(self, name, age, health, hasFur, maneSize):
        super().__init__(name, age, health, hasFur)

        self.__maneSize = maneSize

    @classmethod
    def fromBirth(cls, name, hasFur, maneSize):
        return cls(name, 0, 100, hasFur, maneSize)

    def makeSound(self):
        print('Lion Sound')
    
    def feed(self):
        print('Feeding Lion ..') 

    def getManeSize(self):
        return self.__maneSize


class Giraffe(Mammal):
    def __init__(self, name, age, health, hasFur, neckSize):
        super().__init__(name, age, health, hasFur)

        self.__neckSize = neckSize

    @classmethod
    def fromBirth(cls, name, hasFur, neckSize):
        return cls(name, 0, 100, hasFur, neckSize)

    def makeSound(self):
        print('Giraffe Sound')

    def feed(self):
        print('Feeding Giraffe ..')

    def getNeckSize(self):
        return self.__neckSize


class FlyingFish(Fish, Bird):
    def __init__(self, name, age, health, waterType, canFly, glideDistance):
        Fish.__init__(self, name, age, health, waterType)
        Bird.__init__(self, name, age, health, canFly,)
        self.__glideDistance = glideDistance


    @classmethod
    def fromBirth(cls, name, waterType, canFly, glideDistance):
        return cls(name, 0, 100, waterType, canFly, glideDistance)

    def makeSound(self):
        print('Flying Fish Sound')

    def feed(self):
        print('Feeding Flying Fish ..')

    def getGlideDistnace(self):
        return self.__glideDistance


class Penguin(Bird):
    def __init__(self, name, age, health, canFly, swimmingSpeed):
        super().__init__(name, age, health, canFly)

        self.__swimmingSpeed = swimmingSpeed
    
    @classmethod
    def fromBirth(cls, name, canFly, swimmingSpeed):
        return cls(name, 0, 100, canFly, swimmingSpeed)

    def makeSound(self):
        print('Penguin Sound')

    def feed(self):
        print('Feeding Penguin ..')

    def getSwimmingSpeed(self):
        return self.__swimmingSpeed


class Pigeon(Bird):
    def __init__(self, name, age, health, canFly, homingAbility):
        super().__init__(name, age, health, canFly)
    
        self.__homingAbility = homingAbility

    @classmethod
    def fromBirth(cls, name, canFly, homingAbility):
        return cls(name, 0, 100, canFly, homingAbility)

    def makeSound(self):
        print("Pigeon Sound")

    def feed(self):
        print('Feeding Pigeon ..')

    def getHomingAbility(self):
        return self.__homingAbility


class Snake(Reptile):
    def __init__(self, name, age, health, skinType, venomous):
        super().__init__(name, age, health, skinType)

        self.__venomous = venomous

    @classmethod
    def fromBirth(cls, name, skinType, venomous):
        return cls(name, 0, 100, skinType, venomous)

    def makeSound(self):
        print('Snake Sound')

    def feed(self):
        print('Feeding Snake ..')

    def getVenomStatus(self):
        return self.__venomous


# Simulation
zoo = Zoo('Hadiqat El-Hayawan', 'Gize, Egypt')

eMammals     = Enclosure(50, zoo)
eLions       = Enclosure(50, zoo)
eGiraffes    = Enclosure(50, zoo)
eFlyingFish  = Enclosure(50, zoo)
ePenguins    = Enclosure(50, zoo)
ePigeons     = Enclosure(50, zoo)
eSnakes      = Enclosure(50, zoo)

l1 = Lion('lion1', '12', 90, True, 12)
l2 = Lion('lion2', '20', 40, True, 14)
l3 = Lion('lion3', '40', 50, True, 10)
l4 = Lion('lion4', '30', 60, True, 15)
l5 = Lion('lion5', '25', 70, True, 16)
eLions + l1
eLions + l2
eLions + l3
eLions + l4
eLions + l5

g1 = Giraffe('giraffe1', '12', 100, True, 100)
g2 = Giraffe('giraffe2', '14', 80, True, 90)
g3 = Giraffe('giraffe3', '20', 56, True, 120)
g4 = Giraffe('giraffe4', '30', 70, True, 110)
g5 = Giraffe('giraffe5', '10', 92, True, 90)
eGiraffes + g1
eGiraffes + g2
eGiraffes + g3
eGiraffes + g4
eGiraffes + g5

f1 = FlyingFish('FlyingFish1', 12, 100, 'Salt', True, 10)
f2 = FlyingFish('FlyingFish2', 14, 80, 'Salt', True, 12)
f3 = FlyingFish('FlyingFish3', 20, 56, 'Salt', True, 14)
f4 = FlyingFish('FlyingFish4', 30, 70, 'Salt', True, 9)
f5 = FlyingFish('FlyingFish5', 10, 92, 'Salt', True, 11)
eFlyingFish + f1
eFlyingFish + f2
eFlyingFish + f3
eFlyingFish + f4
eFlyingFish + f5

pen1 = Penguin('penguin1', 6, 100, False, 10)
pen2 = Penguin('penguin2', 8, 80, False, 12)
pen3 = Penguin('penguin3', 10, 56, False, 14)
pen4 = Penguin('penguin4', 12, 70, False, 9)
pen5 = Penguin('penguin5', 14, 92, False, 11)
ePenguins + pen1
ePenguins + pen2
ePenguins + pen3
ePenguins + pen4
ePenguins + pen5

pg1 = Pigeon('pigeon1', 2, 96, True, 10)
pg2 = Pigeon('pigeon2', 4, 80, True, 6)
pg3 = Pigeon('pigeon3', 6, 56, True, 9)
pg4 = Pigeon('pigeon4', 8, 70, True, 8)
pg5 = Pigeon('pigeon5', 10, 92, True, 5)
ePigeons + pg1
ePigeons + pg2
ePigeons + pg3
ePigeons + pg4
ePigeons + pg5

s1 = Snake('snake1', 14, 56, 'dark', True)
s2 = Snake('snake2', 16, 70, 'light', False)
s3 = Snake('snake3', 18, 92, 'dark', True)
s4 = Snake('snake4', 20, 80, 'light', False)
s5 = Snake('snake5', 22, 56, 'dark', False)
eSnakes + s1
eSnakes + s2
eSnakes + s3
eSnakes + s4
eSnakes + s5


emp1 = Veterinarian('Omar Zaid', zoo, True)
emp2 = Zookeeper('Mostafa Raef', zoo, 'Morning')


# Treating Animals
for a in eLions:
    print(a.getName(), a.getHealth())

for a in eLions:
    emp1.treatAnimal(a)


for a in eLions:
    print(a.getName(), a.getHealth())

for a in eLions:
    emp2.feedAnimal(a)

# Moving Animals to another enclosure
print("E1 Animals:")
eLions.getAnimals()
print("E0 Animals")
eMammals.getAnimals()

emp2.moveAnimalToEnclosure(l1, eMammals)

print("E1 Animals:")
eLions.getAnimals()
print("E0 Animals")
eMammals.getAnimals()

print(zoo)