# __init__.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on 8/25/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
__init__.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'


from sqlalchemy import engine as sqlalchemy_engine
from sqlalchemy import exc as sqlalc_errors

from bunch import Bunch

from tsetseDB.utils import errors


class BaseImportSheet(object):
    """
    Base class for import sheets.
    """
    def __init__(self, engine, metadata, worksheet, workbook_path, has_header_row=True):
        """
        Returns instance of `BaseImportSheet` constructed from `worksheet`.
        But should be overridden in child classes.
        :param engine:
        :param metadata:
        :param has_header_row:
        :param worksheet: worksheet object
        :param workbook_path: location of source workbook file
        """

        self.engine = engine
        self.metadata = metadata
        self._active_connection = None
        self.name = worksheet.name
        self.worksheet = worksheet
        self.path = workbook_path
        self.current_row_number = 0
        self.has_header_row = has_header_row
        self._insert_on_table_functions = None

    def _is_known_village(self, village_string):
        """
        Returns `True` if `village_string` matches either a valid village code or name.
        Returns `False` otherwise.
        :param village_string:
        :return:
        """
        if village_string in self.village_id_map.keys():
            return True
        else:
            return False

    def process_rows(self):
        """
        Runs self.process_row() on all rows.
        :return:
        """

        self.set_current_row(0)
        results = []
        while 1:
            if (self.current_row_number <= self.worksheet.nrows - 1) and (self.current_row_number >= 0):
                try:
                    results.append(self.process_row())
                    self.current_row_number += 1
                except sqlalc_errors.IntegrityError as e:
                    if "UNIQUE constraint failed:" in str(e.orig):
                        self.current_row_number += 1
                        continue
                    else:
                        raise
            else:
                break

        return results

    def process_row(self):
        """
        Uses data in row at `self.current_row_number` to create and commit INSERT statements to `self.engine`.
        Returns a `Bunch` containing the `sqlalchemy.engine.Connection.execute()` results for each table INSERTed to.
        :return: `Bunch`
        """

        if self.has_header_row and (self.current_row_number == 0):
            self.current_row_number += 1
        else:
            pass

        connection = self._get_active_connection()
        results = Bunch()

        # Call methods to generate INSERT calls populated with values from the current row
        for insert_on_table_func in self._insert_on_table_functions:
            try:
                results.update(insert_on_table_func(connection))
            except TypeError as e:
                if "'NoneType' object is not callable" in e.message:
                    msg = "You must define 'self._insert_on_table_xxx() functions and append them to " \
                          "the self._insert_on_table_functions in your 'child.__init__()'"
                    raise errors.TsetsedbError(msg)

        return results

    def _get_active_connection(self):
        """
        Returns connection object to `self.engine` if one is stored in `self._active_connection`.
        Creates, stores, and returns one if not.
        :return: `sqlalchemy.engine.Connection` object
        """
        if isinstance(self._active_connection, type(sqlalchemy_engine.Connection)):
            return self._active_connection
        else:
            self._active_connection = self.engine.connect()
            return self._active_connection

    def set_current_row(self, x):
        """
        Sets `self.current_row_number = int(x)` after checking that the sheet goes that far.
        :param x: a row number
        :return: `None`
        """
        x = int(x)

        # worksheet.nrows starts at 1; worksheet.row_values starts at 0
        if (x <= self.worksheet.nrows - 1) and (x >= 0):
            self.current_row_number = x
        else:
            msg = "'x' must be between 0 and %s. You provided: %s" % (self.worksheet.nrows - 1, x)
            raise ValueError(msg)