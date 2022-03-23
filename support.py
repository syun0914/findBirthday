from sys import argv
from findBirthday import find, multiFind as mf

if __name__ == __main__:
    if argv[1] == 'multi':
        try:
            mf(eval(argv[2]), *argv[3:-2], int(argv[-1]))
        except:
            mf(eval(argv[2]), *argv[3:])
    else:
        find(*argv[1:])