'''
Created on 28/10/2015

@author: Joel Pagliuca
'''

import re

__all__ = ['read_class_dump']

#- (int)add:(int)number1 delegate:(int)number2;
METHOD_REGEX = r'[\-\+]\s*\((\*?\w*)\)(\w+)\:\((\*?\w*)\)(\w+)(?:\s+(?:\w*\:)?\((\*?\w*)\)(\w+))*'

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
    
    def hook(self, flag=None):
        '''
        gets the string representing the class
        
        @rtype: str
        '''
        out = ""
        out += "%hook {}".format(self.name)
        for m in self.methods:
            out += m.hook(flag)
        out += "%end"
    
    def __bool__(self):
        return True

class Method(object):
    '''
    a class method
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.class_name = None
        self.signature = None
        self.name = None
        self.type = None
        self.params = []
    
    def hook(self, flag=None):
        '''
        gets the string representing the method
        
        @rtype: str
        '''
        return ""

def read_class_dump(dump):
    '''
    makes a list of HookedClass from the given dump
    dump will be from open(...).readlines()
    
    while not in a class: read until new class
    while in a class: look for: methods, end of class, properties
    
    @param dump: list
    @rtype: list
    '''
    current_class = None
    classes = []
    
    for line in dump:
        if not line:
            continue
        # IN A CLASS
        if current_class:
            if "@end" in line:
                classes.append(current_class)
                current_class = None
                continue

            m = re.match(METHOD_REGEX, line)
            if m:
                method = Method()
                method.class_name = current_class.name
                method.signature = line.strip()
                g = m.groups()
                method.type = g[0]
                method.name = g[1]
                g = g[2:]
                # read the parameters
                while g:
                    method.params.append((g[0], g[1])) # (type, name)
                    g = g[2:]
        # NOT IN A CLASS
        else:
            m = re.match(r'@interface (.+)', line)
            if m:
                current_class = HookedClass()
                current_class.name = m.groups[0]
                continue