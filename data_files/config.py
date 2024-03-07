import os
from configparser import ConfigParser

root_folder = os.path.dirname(os.path.abspath(__file__))
db_ini_name = 'database.ini'
full_address = os.path.join(root_folder, db_ini_name)


def config(filename=full_address, section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)

        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} is not found in the {1} file'.format(section, filename))

    return db