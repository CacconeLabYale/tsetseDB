# column_data.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on 2014-08-21.
#
# Please see the license info in the root folder of this package.

"""
=================================================
column_data.py
=================================================
Purpose:

"""

__author__ = 'Gus Dunn'

from tsetseDB.utils.errors import TsetseDBError


def get_species_name(cell_string, file_name):
    """
    Returns expected species name format given various encountered species IDs
    from the excel files.

    :param cell_string: string from the excel file
    :return: `str`
    """



    try:
        return species_dict[cell_string]
    except IndexError:
        msg = "Encountered unexpected species name '%s' in CSV file '%s'." % (cell_string, file_name)
        raise TsetseDBError(msg)
    except:
        raise
