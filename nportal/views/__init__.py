# views folder registration
import re
from io import StringIO
import csv

TITLE = "HPC Allocations"

SITE_MENU = [
        {'href': '', 'title': 'Home'},
        {'href': 'about.html', 'title': 'About HPC'},
        {'href': 'acme', 'title': TITLE},
        {'href': 'people', 'title': 'People'},
]

# preparers
strip_whitespace = lambda v: v.strip(' \t\n\r') if v is not None else v
# replaces multiple spaces with a single space
remove_multiple_spaces = lambda v: re.sub(' +', ' ', v)


conn_err_msg = """\
        The application is having a problem using your SQL database.
        The problem might be caused by one of the following things:

        1.  You may need to run the "initialize_allocations_db" script
            to initialize your database tables.  Check your virtual
            environment's "bin" directory for this script and try to run it.

        2.  Your database server may not be running.  Check that the
            database server referred to by the "sqlalchemy.url" setting in
            your "development.ini" file is running.

        After you fix the problem, please restart the application to
        try it again.
        """


class CSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        fout = StringIO()

        writer = csv.writer(fout, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(value['headers'])
        writer.writerows(value['rows'])

        resp = system['request'].response
        resp.content_type = 'text/csv'
        resp.content_disposition = 'attachment;filename="report.csv"'
        return fout.getvalue()


default_change = """

"""
