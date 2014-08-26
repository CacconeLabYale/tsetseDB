# errors.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on 2014-08-21.
#
# Please see the license info in the root folder of this package.

"""
=================================================
errors.py
=================================================
Purpose:

"""

__author__ = 'Gus Dunn'


class TsetseDBError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)