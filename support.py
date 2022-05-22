from sys import argv
from main import fb, mf

if __name__ == '__main__':
    if argv[1] == 'multi': # main.multiFind
        try:
            mf(eval(argv[2]), *argv[3:-2], int(argv[-1]))
        except:
            mf(eval(argv[2]), *argv[3:])
    else: # main.find
        fb(*argv[1:])