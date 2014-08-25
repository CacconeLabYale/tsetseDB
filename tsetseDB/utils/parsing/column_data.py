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
import re

import arrow

from tsetseDB.utils.errors import TsetseDBError
from tsetseDB.utils import constants as c

# import species abbreviation to long name dictionary
species_dict = c.get_species_abbrv_conversion_dict()

# import village to village_id conversion dict
village_id_map = c.get_village_id_map()


def convert_species_name(cell_string, file_name):
    """
    Returns expected species name format given various encountered species IDs
    from the excel files.

    :param cell_string: string containing a species
    :param file_name:
    :return: `str`
    """

    try:
        return species_dict[cell_string]
    except IndexError:
        msg = "Encountered unexpected species name '%s' in CSV file '%s'." % (cell_string, file_name)
        raise TsetseDBError(msg)
    except:
        raise


def convert_date_dd_mm_yy(cell_string, file_name):
    """

    :param cell_string:
    :param file_name:
    :return:
    """

    d = cell_string.lstrip("'")
    d1 = list(reversed([int(x) for x in re.findall(r"[\d']+", d)]))
    d1[0] += 2000

    date = arrow.get(*d1)

    return date.format("YYYY-MM-DD")
