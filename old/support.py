from sys import argv
from platform import system
from asyncBirthday import find as f, multiFind as mf
from findBirthday import find as of, multiFind as omf
from asyncio import run

if system() == 'Windows':
    from asyncio import (
        set_event_loop_policy as setPolicy,
        WindowsSelectorEventLoopPolicy as EventLoopPolicy
    )
    setPolicy(EventLoopPolicy())

if __name__ == '__main__':
    if argv[1] == 'old': # findBirthday.find
        of(*argv[2:])
    if argv[1] == 'omulti': # findBirthday.multiFind
        try:
            omf(eval(argv[2]), *argv[3:-2], int(argv[-1]))
        except:
            omf(eval(argv[2]), *argv[3:])

    if argv[1] == 'multi': # asyncBirthday.multiFind
        try:
            run(mf(eval(argv[2]), *argv[3:-2], int(argv[-1])))
        except:
            run(mf(eval(argv[2]), *argv[3:]))
    else: # asyncBirthday.find
        run(f(*argv[1:]))