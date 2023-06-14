from os import name

#clear the screen
def clearScreen() -> None:
    ostype = name
    if ostype == 'nt':
        clear = 'cls'
    elif ostype == 'posix':
        clear = 'clear'
    system(clear)