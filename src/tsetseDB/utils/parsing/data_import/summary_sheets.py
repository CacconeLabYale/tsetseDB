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

from bunch import Bunch

from tsetseDB.utils.parsing import column_data as cdata
from tsetseDB.utils.parsing.data_import import BaseImportSheet
from tsetseDB.utils import errors
from tsetseDB.utils.constants import get_village_id_map, get_village_ids


class SummarySheet(BaseImportSheet):
    """
    Class to manage importing data from Robert's "survey summary" type excel sheets.
    """
    def __init__(self, engine, metadata, worksheet, workbook_path, season, trap_type='biconical', has_header_row=True):
        """
        Returns instance of `SummarySheet` constructed from `worksheet`.
        :param engine:
        :param metadata:
        :param season:
        :param trap_type:
        :param has_header_row:
        :param worksheet: worksheet object
        :param workbook_path: location of source workbook file
        """

        # Calling base class __init__ for the rest.
        BaseImportSheet.__init__(self, engine, metadata, worksheet, workbook_path, has_header_row=True)

        # Extending the base class __init__ for the rest
        self.season = season
        self.trap_type = trap_type
        self.village_id_map = get_village_id_map()
        self.village_ids = get_village_ids()
        self._insert_on_table_functions = [self._insert_on_trap,
                                           self._insert_on_village]

    def _build_trap_row(self, worksheet_row):
        """
        Builds data that can be added to a `trap` table.
        Returns a `dict`.
        :param worksheet_row:
        :return: `dict`
        """
        trap_row_dict = dict()

        trap_row_dict['trap_number'] = self._get_trap_no(worksheet_row=worksheet_row)
        trap_row_dict['season'] = self.season
        trap_row_dict['deploy_date'] = self._get_trap_deployed_on(worksheet_row=worksheet_row,
                                                                  return_as='datetime.date')
        trap_row_dict['removal_date'] = self._get_trap_removed_on(worksheet_row=worksheet_row,
                                                                  return_as='datetime.date')
        trap_row_dict['trap_type'] = self.trap_type
        # get village NAME and convert to ID
        trap_row_dict['village_id'] = self.village_id_map[self._get_village(worksheet_row=worksheet_row)]
        trap_row_dict['gps_coords'] = self._get_trap_latlong(worksheet_row=worksheet_row)
        trap_row_dict['elevation'] = self._get_trap_elevation(worksheet_row=worksheet_row)
        #trap_row_dict['trap_id'] = "%s:%s" % (trap_row_dict["deploy_date"], trap_row_dict["gps_coords"])
        trap_row_dict['other_info'] = self._get_other_info(worksheet_row=worksheet_row)

        return trap_row_dict

    def _build_village_row(self, worksheet_row):
        """
        Builds data that can be added to a `village` table.
        Returns a `dict`.
        :param worksheet_row:
        :return: `dict`
        """
        village_row_dict = dict()

        # get village NAME and convert to ID
        village_row_dict['village_id'] = self.village_id_map[self._get_village(worksheet_row=worksheet_row)]
        village_row_dict["district"] = self._get_district(worksheet_row=worksheet_row)
        village_row_dict["county"] = self._get_county(worksheet_row=worksheet_row)
        village_row_dict["subcounty"] = self._get_subcounty(worksheet_row=worksheet_row)
        village_row_dict["parish"] = self._get_parish(worksheet_row=worksheet_row)
        village_row_dict["village_name"] = self._get_village(worksheet_row=worksheet_row)

        return village_row_dict

    def _insert_on_trap(self, connection):
        results = Bunch()

        # Generate INSERT calls populated with values from the current row for Trap table and submit to
        trap_table = self.metadata.tables['trap']

        trap_insert_values = self._build_trap_row(self.worksheet.row_values(self.current_row_number))
        trap_insert_obj = trap_table.insert(values=trap_insert_values)
        results.trap = connection.execute(trap_insert_obj)

        return results

    def _insert_on_village(self, connection):
        results = Bunch()

        # Generate INSERT calls populated with values from the current row for Village table and submit to
        village_table = self.metadata.tables['village']

        village_insert_values = self._build_village_row(self.worksheet.row_values(self.current_row_number))
        village_insert_obj = village_table.insert(values=village_insert_values)
        results.village = connection.execute(village_insert_obj)

        return results

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

    def _get_parish(self, worksheet_row):
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
        village_string = worksheet_row[4]

        if self._is_known_village(village_string):
            pass
        else:
            msg = "%s, from data summary sheet: %s and row number: %s, is not currently a recognized village." % \
                (village_string,
                 self.worksheet.name,
                 self.current_row_number + 1)

            raise errors.TsetsedbImportError(msg)

        if village_string in self.village_ids:
            # we say we return the NAME not ID so lets make sure we do.
            return self.village_id_map[village_string]
        else:
            return village_string

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

    def _get_trap_deployed_on(self, worksheet_row, return_as='datetime.date'):
        """
        Extracts trap's deploy date from summary sheet row.

        :param return_as:
        :param worksheet_row:
        :return:
        """
        return cdata.convert_date_dd_mm_yy(worksheet_row[11], return_as=return_as)

    def _get_trap_removed_on(self, worksheet_row, return_as='datetime.date'):
        """
        Extracts trap's removal date from summary sheet row.

        :param return_as:
        :param worksheet_row:
        :return:
        """
        return cdata.convert_date_dd_mm_yy(worksheet_row[12], return_as=return_as)

    def _get_other_info(self, worksheet_row):
        """
        Extracts "other info" column from summary sheet row.

        :param worksheet_row:
        :return:
        """
        return worksheet_row[-1]
