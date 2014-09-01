# test_summary_sheets.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 8/27/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
test_summary_sheets.py
=================================================
Purpose:

"""

__author__ = 'Gus Dunn'

from nose.tools import raises

from sqlalchemy import exc

from pkg_resources import Requirement, resource_filename

from tsetseDB.utils.database_description import get_engine
from spartan.utils import spreadsheets as ss

from tsetseDB.utils.parsing.data_import.summary_sheets import SummarySheet

wb = resource_filename(Requirement.parse("tsetseDB"), "test_data/dissection_workbook.xls")
wb = ss.get_workbook(wb)
ws = wb.sheet_by_name('summary_test_sheet_1')


class TestSummarySheets(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        self.engine, self.metadata = get_engine("sqlite://")

    def teardown(self):
        pass

    def test_SummarySheet_creation(self):
        summary = SummarySheet(engine=self.engine, metadata=self.metadata, worksheet=ws, workbook_path=wb,
                               season='wet', trap_type='biconical', has_header_row=True)

    def test_SummarySheet_process_row(self):

        summary = SummarySheet(engine=self.engine, metadata=self.metadata, worksheet=ws, workbook_path=wb,
                               season='wet', trap_type='biconical', has_header_row=True)
        results = summary.process_row()

    def test_SummarySheet_process_rows(self):

        summary = SummarySheet(engine=self.engine, metadata=self.metadata, worksheet=ws, workbook_path=wb,
                               season='wet', trap_type='biconical', has_header_row=True)
        results = summary.process_rows()

        return results

    @raises(exc.IntegrityError)
    def test_SummarySheet_process_row_season_integrity(self):

        summary = SummarySheet(engine=self.engine, metadata=self.metadata, worksheet=ws, workbook_path=wb,
                               season='nope', trap_type='biconical', has_header_row=True)
        results = summary.process_row()

    @raises(exc.IntegrityError)
    def test_SummarySheet_process_row_trap_type_integrity(self):

        summary = SummarySheet(engine=self.engine, metadata=self.metadata, worksheet=ws, workbook_path=wb,
                               season='wet', trap_type='nope', has_header_row=True)
        results = summary.process_row()


def run_summary_sheet_as_far_as_you_can(sqlite_uri=None):
    """
    meant to be run in ipython to look at results of the run or to build a sqlite version of the db to examine.
    If `sqlite_uri` is `None`, build db in memory.
    :param sqlite_uri: address of an on disk version of the db to build.
    :return:
    """
    from pkg_resources import Requirement, resource_filename

    from tsetseDB.utils.database_description import get_engine
    from spartan.utils import spreadsheets as ss

    from tsetseDB.utils.parsing.data_import.summary_sheets import SummarySheet

    wb = resource_filename(Requirement.parse("tsetseDB"), "test_data/dissection_workbook.xls")
    wb = ss.get_workbook(wb)
    ws = wb.sheet_by_name('summary_test_sheet_1')

    if not sqlite_uri:
        sqlite_uri = 'sqlite://'
    else:
        pass

    engine, metadata = get_engine(sqlite_uri, echo=False, checkfirst=True)

    summary = SummarySheet(engine=engine, metadata=metadata, worksheet=ws, workbook_path=wb,
                           season='wet', trap_type='biconical', has_header_row=True)
    results = summary.process_rows()

    return results

if __name__ == "__main__":
    import docopt

    usage = """

    Usage:
    test_summary_sheets.py [SQLITE_URI]

    Arguments:
      SQLITE_URI     location of sqlite db to create. Default: in memory

    Options:
      -h --help    show this

    """

    args = docopt.docopt(usage)

    results = run_summary_sheet_as_far_as_you_can(sqlite_uri=args['SQLITE_URI'])