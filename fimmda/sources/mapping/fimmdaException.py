#!/usr/bin/env python
# encoding: utf-8
"""
exceptions.py
"""
class ExceptionTemplate(Exception):
    def __call__(self, *args):
		
        return self.__class__(*(self.args + args))
		
class FimmdaException(ExceptionTemplate):
	pass

ERROR_101 = "[ERROR-101] Cannot recognize the file"
ERROR_102 = "[ERROR-102] Error when trying to write into the file!"
ERROR_103 = "[ERROR-103] Error when trying to open the file!"
ERROR_104 = "[ERROR-104] There is nothing in the source file"
