import os


'''
function to clear the terminal
'''
def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def print_menu():
    print('1. Stand')
    print('2. Hit')
    print('3. Split')


def main():
    print('Hello World')


if __name__ == '__main__':
    main()
