from sys import argv
from findBirthday import unFind, find

if argv[1] == 'un':
    try:
        unFind(eval(argv[2]), *argv[3:-2], int(argv[-1]))
    except:
        unFind(eval(argv[2]), *argv[3:])
else:
<<<<<<< HEAD
    find(*argv[1:])
=======
    find(*argv[1:])
>>>>>>> 31b6745731d0fa5e88a8171e7aba78a291135cd5
