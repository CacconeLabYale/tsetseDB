# dissection_sheets.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 8/28/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
dissection_sheets.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

from bunch import Bunch

from tsetseDB.utils.constants import get_species_abbrv_conversion_dict
from tsetseDB.utils.parsing import column_data as cdata
from tsetseDB.utils.parsing.data_import import BaseImportSheet
from tsetseDB.utils import errors
from tsetseDB.utils import constants


class DissectionSheet(BaseImportSheet):
    """
    Class to manage importing data from Robert's "survey summary" type excel sheets.
    """
    def __init__(self, engine, metadata, worksheet, workbook_path, has_header_row=True):
        """
        Returns instance of `DissectionSheet` constructed from `worksheet`.
        :param engine:
        :param metadata:
        :param has_header_row:
        :param worksheet: worksheet object
        :param workbook_path: location of source workbook file
        """

        # Calling base class __init__ for the rest.
        BaseImportSheet.__init__(self, engine, metadata, worksheet, workbook_path, has_header_row=True)

        # Extending the base class __init__ for the rest
        self.species_abbrv_conversion_dict = get_species_abbrv_conversion_dict()
        self.village_ids = constants.get_village_ids()
        self.village_id_map = constants.get_village_id_map()
        self._insert_on_table_functions = [self._insert_on_fly,
                                           # self._insert_on_tube,
                                           ]

    def _build_fly_row(self, worksheet_row):
        """

        :param worksheet_row:
        """
        
        fly_row_dict = dict()
        
        fly_row_dict["village_id"] = self._get_village(worksheet_row)
        fly_row_dict["collection_number"] = self._get_collection_number(worksheet_row)
        fly_row_dict["sex"] = self._get_sex(worksheet_row)
        fly_row_dict["species"] = self._get_species(worksheet_row)
        fly_row_dict["hunger_stage"] = self._get_hunger_stage(worksheet_row)
        fly_row_dict["wing_fray"] = self._get_hunger_stage(worksheet_row)
        fly_row_dict["box_id"] = -1  # assigns to special staging "box"
        tissue_results = self._get_positive_tissues(worksheet_row)
        fly_row_dict["infected"] = self._get_infected_status(tissue_results)
        fly_row_dict["positive_proboscis"] = tissue_results.proboscis
        fly_row_dict["positive_midgut"] = tissue_results.midgut
        fly_row_dict["positive_salivary_gland"] = tissue_results.salivary
        fly_row_dict["tryps_by_scope"] = fly_row_dict["infected"]
        fly_row_dict["date_of_collection"] = self._get_date_of_collection(worksheet_row)
        fly_row_dict["gps_coords"] = self._get_trap_latlong(worksheet_row)
        fly_row_dict["teneral"] = self._get_teneral(worksheet_row)
        fly_row_dict["comments"] = self._get_comments(worksheet_row)

        import pdb
        pdb.set_trace()
        return fly_row_dict

    # def _build_tube_row(self, worksheet_row):
    #     """
    #
    #     :param worksheet_row:
    #     """
    #     tube_row_dict = dict()
    #
    #     tube_row_dict["contents"] = self._get_solution()
    #     tube_row_dict["solution"] = self.
    #     tube_row_dict["fly_id"] = self.
    #     tube_row_dict["box_id"] = self.
    #     tube_row_dict["parent_id"] = self.
        
    def _insert_on_fly(self, connection):
        results = Bunch()

        # Generate INSERT calls populated with values from the current row for fly table and submit to
        fly_table = self.metadata.tables['fly']

        fly_insert_values = self._build_fly_row(self.worksheet.row_values(self.current_row_number))
        fly_insert_obj = fly_table.insert(values=fly_insert_values)
        results.fly = connection.execute(fly_insert_obj)

        return results

    # def _insert_on_tube(self, connection):
    #     results = Bunch()
    #
    #     # Generate INSERT calls populated with values from the current row for tube table and submit to
    #     tube_table = self.metadata.tables['tube']
    #
    #     tube_insert_values = self._build_tube_row(self.worksheet.row_values(self.current_row_number))
    #     tube_insert_obj = tube_table.insert(values=tube_insert_values)
    #     results.tube = connection.execute(tube_insert_obj)
    #
    #     return results
        
    def _get_village(self, worksheet_row):
        """
        Extracts village name from summary sheet row.

        :param worksheet_row:
        :return:
        """
        village_string = worksheet_row[0]

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
        Extracts trap number from dissection sheet row.

        :param worksheet_row:
        :return:
        """
        return int(worksheet_row[1])

    def _get_trap_latlong(self, worksheet_row):
        """
        Extracts trap's latitude and longitude from dissection sheet row.

        :param worksheet_row:
        :return:
        """
        lat = worksheet_row[2]
        lon = worksheet_row[3]

        return "%s:%s" % (lat, lon)

    def _get_date_of_collection(self, worksheet_row, return_as='datetime.date'):
        """
        Extracts fly's collection date from dissection sheet row.

        :param return_as:
        :param worksheet_row:
        :return:
        """
        return cdata.convert_date_dd_mm_yy(worksheet_row[4], return_as=return_as)

    def _get_species(self, worksheet_row):
        """
        Extracts fly's species from dissection sheet row.

        :param worksheet_row:
        :return:
        """
        return self.species_abbrv_conversion_dict(worksheet_row[5])

    def _get_sex(self, worksheet_row):
        """
        Extracts fly's sex from dissection sheet row.

        :param worksheet_row:
        :return:
        """
        sex_dict = {"M": "M",
                    "F": "F",
                    "MALE": "M",
                    "FEMALE": "F"}

        return sex_dict[worksheet_row[6].upper()]

    def _get_teneral(self, worksheet_row):
        """
        Extracts fly's teneral status from dissection sheet row.

        :param worksheet_row:
        :return:
        """
        teneral_dict = {"T": True,
                       "NT": False, }

        return teneral_dict[worksheet_row[7].upper()]

    def _get_collection_number(self, worksheet_row):
        """
        Extracts fly's ID number for the collection from dissection sheet row.

        :param worksheet_row:
        :return:
        """

        return int(cdata.convert_tube_code(worksheet_row[8]))

    def _get_hunger_stage(self, worksheet_row):
        """
        Extracts fly's hunger stage for the collection from dissection sheet row.

        :param worksheet_row:
        :return:
        """

        if worksheet_row[8] in ['1', '2', '3', '4']:
            return worksheet_row[8]
        else:
            return "NA"

    def _get_positive_tissues(self, worksheet_row):
        """
        Extracts fly's tissue infection status from dissection sheet row.

        :param worksheet_row:
        :return:
        """
        proboscis, midgut, salivary = worksheet_row[9:12]

        tissues = Bunch()

        tissues.proboscis = constants.infection_status_conversion[proboscis]
        tissues.midgut = constants.infection_status_conversion[midgut]
        tissues.salivary = constants.infection_status_conversion[salivary]

        return tissues

    def _get_wing_fray(self, worksheet_row):
        """
        Extracts fly's wing fray for the collection from dissection sheet row.

        :param worksheet_row:
        :return:
        """

        if worksheet_row[12] in ['1', '2', '3', '4']:
            return worksheet_row[12]
        else:
            return "NA"

    def _get_solution(self, worksheet_row):
        """
        Extracts storage solution from dissection sheet row.

        :param worksheet_row:
        :return:
        """

        return worksheet_row[13]

    def _get_comments(self, worksheet_row):
        """
        Extracts comments info from dissection sheet row.

        :param worksheet_row:
        :return:
        """

        return worksheet_row[14]

    def _get_infected_status(self, tissue_results):
        """
        Based on tissue results return either ['positive', 'negative', 'not dissected']

        :param worksheet_row:
        :return:
        """

        results = set(tissue_results.values())

        if "positive" in results:
            return "positive"
        elif "not dissected" in results:
            return "not dissected"
        else:
            return "negative"