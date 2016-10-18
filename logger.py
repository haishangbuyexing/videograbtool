import logging
l = logging.getLogger("")
def debug(txt, *f):
    try:
        l.debug(txt, *f)
        print( txt % f )
    except:
        pass

def info(txt, *f):
    try:
        l.info(txt, *f)
        print( txt % f )
    except:
        pass

def warning(txt, *f):
    try:
        l.warning(txt, *f)
        print( txt % f )
    except:
        pass

def error(txt, *f):
    try:
        l.error(txt, *f)
        print( txt % f )
    except:
        pass

def critical(txt, *f):
    try:
        l.critical(txt, *f)
        print( txt % f )
    except:
        pass
