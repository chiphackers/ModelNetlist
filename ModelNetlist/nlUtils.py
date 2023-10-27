import matplotlib
matplotlib.use('Agg')

from matplotlib import pylab

import networkx as nx
import matplotlib.pyplot as plt

##############################################################################
# Debug prints
##############################################################################
def shout(severity, message):
    """
    Print messages to standard output
    """
    if severity == 'SILENT':
        return

    if severity == 'WARN':
        print('%s[WARN ]: %s %s' % ('\033[93m', message, '\033[0m'))
    elif severity == 'ERROR':
        print('%s[ERROR]: %s %s' % ('\033[91m', message, '\033[0m'))
        sys.exit(-1)
    elif severity == 'INFO':
        print('%s[INFO ]: %s %s' % ('\033[92m', message, '\033[0m'))

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate
