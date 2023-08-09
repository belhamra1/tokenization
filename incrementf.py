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