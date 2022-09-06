import hashlib
import sys
import os

def hash_calculator(data):
    md5 = hashlib.md5(data.encode('utf-8'))
    return md5.hexdigest()

def main():
    banner = """
            Hash generator, select the type to calculate:
            1. String
            2. File
            
    """
    print(banner)
    choice = input("Please select: ")
    if choice == '1':
        data = input('Input your text here:\n')
        print(hash_calculator(data))
    elif choice == '2':
        filepath = input('Input your file path here: \n')
        if not os.path.exists(filepath):
            print('The file does not exist')
            sys.exit()
        with open(filepath, 'rb') as f:
            print(hash_calculator(f.read()))
    else:
        print('Wrong choice, now exit the program')
        sys.exit()

if __name__ == '__main__':
    main()
    