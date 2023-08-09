from mainthing import *

'''def generer_nombre_aleatoire():
    # Remplacez cette fonction par votre propre fonction qui génère des nombres aléatoires
    return random.randint(1, 100)
'''


import random


def read_counter_from_file(increment):
    try:
        with open(increment, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        # If the file does not exist, return 0 and create the file with initial value 0.
        write_counter_to_file(increment, 0)
        return 0

def write_counter_to_file(increment, counter):
    with open(increment, 'w') as file:
        file.write(str(counter))

# Example usage:
increment = 'incrementc.txt'
j = read_counter_from_file(increment)
print("Current value of i:", j)

# Increment j
j += 1

# Write the updated value of i back to the file
write_counter_to_file(increment, j)


############################################################################
'''def add_zero_alternating(number):
    number_str = str(number)
    turns = 0
    while len(number_str) < 16:
        if turns % 2 == 0:
            random_digit = str(random.randint(1, 9))  # Generate a random digit between 1 and 9 (inclusive)
            number_str = random_digit + number_str
        else:
            random_digit = str(random.randint(0, 9))  # Generate a random digit between 0 and 9 (inclusive)
            number_str = number_str + random_digit
        turns += 1


    modified_number = int(number_str)

    return modified_number '''









class MinimalStandardGenerator:
    def __init__(self, seed=1):
        self.a = 16807
        self.m = 2**31 - 1
        self.seed = seed #le premier element cad x0

    def generate(self):
        self.seed = (self.a * self.seed) % self.m
        return self.seed


def get_last_random_number(j):
    generator = MinimalStandardGenerator(seed=1)
    last_random_number = 0
    
   
    for _ in range(j):
        random_number = generator.generate()
        
    last_random_number = random_number**3

    

    while(len(str(last_random_number)) <16):
       last_random_number=int(last_random_number)
       last_random_number +=1

    
    last_random_number=int(str(last_random_number)[:16])
  

    return last_random_number



def tester_repetition(n):
    generated_numbers = {}  # Utilisation d'un dictionnaire pour stocker les valeurs générées
    for _ in range(n):
        
        # Example usage:
        increment = 'incrementc.txt'
        j = read_counter_from_file(increment)
        #print("Current value of i:", j)

        # Increment j
        j += 1

        # Write the updated value of i back to the file
        write_counter_to_file(increment, j)
        nouveau_nombre = get_last_random_number(j)
        if nouveau_nombre in generated_numbers:
            print(f"La valeur {nouveau_nombre} se répète !")
        generated_numbers[nouveau_nombre] = True

tester_repetition(10)  # Testez avec le nombre de valeurs que vous souhaitez générer
