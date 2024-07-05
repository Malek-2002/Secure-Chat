PATH = "D:\Disk\Study\College\CMP 3\Second Term\Courses\[CS] Cryptography & Security\Project\CTF\CTF-4 (Bit Shifting)\\"

def read_file_binary(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    # Convert each byte into its binary representation and concatenate them into a single string
    binary_string = ''.join(format(byte, '08b') for byte in data)
    # Convert the binary string into a list of individual bits
    return [bit for bit in binary_string]

def print_binary_data(data, byte_delimiter=''):
    for bit in data:
        print(bit, end=byte_delimiter)  # Print each bit
    print()  # Print a newline at the end

def roll_left(data, shift_amount):
    # Calculate the effective shift amount (in case it's larger than the length of the data)
    shift_amount %= len(data)
    
    # Roll the data to the left by the shift amount
    rolled_data = data[shift_amount:] + data[:shift_amount]
    
    return rolled_data

def roll_right(data, shift_amount):
    # Calculate the effective shift amount (in case it's larger than the length of the data)
    shift_amount %= len(data)
    
    # Roll the data to the right by the shift amount
    rolled_data = data[-shift_amount:] + data[:-shift_amount]
    
    return rolled_data

def binary_to_string(binary_data):
    # Convert the list of bits to a string
    return ''.join(chr(int(''.join(bit), 2)) for bit in zip(*[iter(binary_data)]*8))


def brute_force_roll(binary_data):
    for i in range(1, len(binary_data) + 1):
        # Roll left and right
        rolled_left = roll_left(binary_data, i)
        rolled_right = roll_right(binary_data, i)
        
        # Convert binary data to string
        rolled_left_str = ''.join(rolled_left)
        rolled_right_str = ''.join(rolled_right)

        # Print rolled data
        print(f"--------------------")
        print(f"Shift amount: {i}")
        print(f"--------------------")
        print("Rolled left:", binary_to_string(rolled_left_str))
        print("Rolled right:", binary_to_string(rolled_right_str))
        print()  # Add a blank line between iterations
        input()

def main():
    filename = PATH + "bits.txt"
    binary_data = read_file_binary(filename)
    print("Original")
    print_binary_data(binary_data)
    brute_force_roll(binary_data)
    print(len(binary_data))

    

if __name__ == "__main__":
    main()
