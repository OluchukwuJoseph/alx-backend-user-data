import logging
import logging.config

# print(logging.DEBUG)
# print(logging.INFO)
# print(logging.WARNING)
# print(logging.ERROR)
# print(logging.CRITICAL)

logging.basicConfig(filename='person.log', level=logging.DEBUG, format='[HOLBERTON] %(asctime)s:%(levelname)s:%(message)s')

class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"My name is {self.name} and i am {self.age} years old."
    
person1 = Person('Chinedu', 20)
logging.info(person1)
