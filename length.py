def number_length(number):
    if number == 0:
        return 1
    return len(str(abs(number)))

# Example usage:
num = 12345
length = number_length(num)
print(f"The length of {num} is: {length}")
