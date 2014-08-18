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
    """
    Table class to store data associated with individual flies:
    - id (int)
    - location_symbol (str)
    - collection_number (int)
    - sex (M|F)
    - species (f|p|m)
    - hunger_stage (1|2|3)
    - wing_fray (int)
    - stored_in (str)
    - box_id (ForeignKey?)
    - infected (bool)
    - tryps_by_scope (bool)
    - tryps_by_pcr (bool)
    - collection_date (date)
    - trap_id (int, ForeignKey?)
    - gps_coords (link to TrapTable)
    - tissues (ask aiden)
    - teneral (bool)
    - comments (str)
    """
    __tablename__ = 'fly'
    id = Column("fly_id", types.Integer, primary_key=True)
    created_on = Column("created_on", types.DateTime)
    modified_on = Column("modified_on", types.DateTime)


class Village(base):
    """
    Table class to store data associated with a single village:
    - id (int)
    - district
    - county
    - subcounty
    - parish
    - name

    """
    __tablename__ = 'village'
    id = Column("village_id", types.Integer, primary_key=True)
    created_on = Column("created_on", types.DateTime)
    modified_on = Column("modified_on", types.DateTime)


class Trap(base):
    """
    Table class to store data associated with a single trap:
    - id (int)
    - season (wet|dry)
    - deploy_date
    - removal_date
    - trap_type (biconical|other?)
    - village_id (ForKey?)
    -
    """
    __tablename__ = 'trap'
    id = Column("trap_id", types.Integer, primary_key=True)
    created_on = Column("created_on", types.DateTime)
    modified_on = Column("modified_on", types.DateTime)


class Tube(base):
    """
    Table class to store data associated with a single storage tube:
    -
    """
    __tablename__ = 'tube'
    id = Column("tube_id", types.Integer, primary_key=True)
    created_on = Column("created_on", types.DateTime)
    modified_on = Column("modified_on", types.DateTime)


class Box(base):
    """
    Table class to store data associated with a freezer box where tubes are stored:
    -
    """
    __tablename__ = 'box'
    id = Column("box_id", types.Integer, primary_key=True)
    created_on = Column("created_on", types.DateTime)
    modified_on = Column("modified_on", types.DateTime)