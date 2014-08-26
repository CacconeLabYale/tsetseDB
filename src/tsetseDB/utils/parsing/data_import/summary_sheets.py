# summary_sheets.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on 8/25/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
summary_sheets.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

#from spartan.utils import spreadsheets as ss
from tsetseDB.utils.parsing import column_data as cdata

# TODO: Convert below functions into a single class that logs file names etc for useful error reporting


class SummarySheet(object):

    def __init__(self, worksheet, workbook_path):
        """
        Returns instance of `SummarySheet` constructed from `worksheet`.
        :param worksheet: worksheet object
        :param workbook_path: location of source workbook file
        """

        self.name = worksheet.name
        self.worksheet = worksheet
        self.path = workbook_path

    def _validate_summary_data_format(self):
        """
        Returns `True` if `worksheet` passes format tests, `False` otherwise.
        :return: `bool`
        """
        raise NotImplementedError()

    def _get_district(self, worksheet_row):
        """
        Extracts district name from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[0]

    def _get_county(self, worksheet_row):
        """
        Extracts county name from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[1]

    def _get_subcounty(self, worksheet_row):
        """
        Extracts district name from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[2]

    def _get_parrish(self, worksheet_row):
        """
        Extracts district name from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[3]

    def _get_village(self, worksheet_row):
        """
        Extracts village name from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[4]

    def _get_trap_no(self, worksheet_row):
        """
        Extracts trap number from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return int(worksheet_row[5])

    def _get_trap_latlong(self, worksheet_row):
        """
        Extracts trap's latitude and longitude from summary sheet row.

        :param worksheet_row:
        :return:
        """
        lat = worksheet_row[6]
        lon = worksheet_row[7]

        return "%s:%s" % (lat, lon)

    def _get_trap_elevation(self, worksheet_row):
        """
        Extracts trap elevation from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return float(worksheet_row[8])

    def _get_trap_human_activity(self, worksheet_row):
        """
        Extracts human activity near trap from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[9]

    def _get_trap_vegetation(self, worksheet_row):
        """
        Extracts vegetation-type near trap from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[10]

    def _get_trap_deployed_on(self, worksheet_row):
        """
        Extracts trap's deploy date from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return cdata.convert_date_dd_mm_yy(worksheet_row[11])

    def _get_trap_removed_on(self, worksheet_row):
        """
        Extracts trap's removal date from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return cdata.convert_date_dd_mm_yy(worksheet_row[12])

    def _get_other_info(self, worksheet_row):
        """
        Extracts "other info" column from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[-1]
