'''
Created on 28/10/2015

@author: Joel Pagliuca
'''

class HookedClass(object):
    '''
    represents a class we will hook
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = None
        self.methods = []

class Method(object):
    '''
    a class method
    '''
    
    def __init__(self):
        '''
        Constructor
        '''