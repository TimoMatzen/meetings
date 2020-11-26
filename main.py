

import confidence
from src import utils, parser, postgres

config = confidence.load_name("meetings")

con = postgres.DBConnection(**config.database)
postgres.create_tables(con)


with con.cursor() as c:
    for file in utils.plt_files(config.data_root):
        user_id = utils.get_user(file)
        for lat, lon, _, d, t in parser.read_file(file):
            if event := parser.parse(user_id, lat, lon, d, t):
                postgres.insert_event(c, event)
    con.connection.commit()