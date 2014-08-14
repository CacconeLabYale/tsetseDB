# database_description.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on Thu Aug 14 17:31:36 EDT 2014.
#
# Please see the license info in the root folder of this package.

"""
=================================================
database_description.py
=================================================
Purpose:

"""

__author__ = 'Gus Dunn'

import os
import sys
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import types


base = declarative_base()

class Fly(base):
    __tablename__ = 'fly'
    id = Column("fly_id", types.Integer, primary_key=True)
    created_on = Column("created_on", types.DateTime)
    modified_on = Column("modified_on", types.DateTime)