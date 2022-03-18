from sys import argv
from findBirthday import unFind, find

if argv[1] == 'un':
    try:
        unFind(eval(argv[2]), *argv[3:-2], int(argv[-1]))
    except:
        unFind(eval(argv[2]), *argv[3:])
else:
    find(*argv[1:])