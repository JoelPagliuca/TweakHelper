#!/usr/bin/env python
# encoding: utf-8
'''
TweakHelper -- Helps you make THEOS tweaks

TweakHelper is a tool for making Tweaks

@author:     Joel Pagliuca

@copyright:  2015 Joel Pagliuca. All rights reserved.

@license:    Creative Commons

@contact:    PagliucaJoel@gmail.com
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from ClassHook import *

__all__ = []
__version__ = 0.1
__date__ = '2015-10-28'
__updated__ = '2015-10-28'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Joel Pagliuca on %s.
  Copyright 2015 Joel Pagliuca. All rights reserved.
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        
        parser.add_argument("-d", "--dump", dest="dump", required=True)
        parser.add_argument("-o", "--output", dest="output", help="write to a file [default: stdout]", default="")

        # Process arguments
        args = parser.parse_args()
        
        dump = args.dump
        output = sys.stdout
        if args.output:
            output = open(args.output, 'w')
        
        # Do stuff
        dump = open(dump, "r").readlines()
        hooks = parse_class_dump(dump)
        for h in hooks:
            output.write(h.hook())
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())