import contextlib

import psycopg2
import psycopg2.extras
from src.models import Event


class DBConnection:
    """
    Database connection object for creating a quick database connection
    """

    def __init__(self, host, dbname, user, password, schema="public", port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.schema = schema
        self.port = port
        self._connection = None

    @contextlib.contextmanager
    def cursor(self):
        """.
        :return:.
        """
        cursor = self.connection.cursor()
        cursor.execute("SET search_path TO %s", (self.schema,))

        yield cursor

        self.connection.commit()

    @property
    def connection(self):
        if self._connection is None:
            self._connection = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port,
            )
        return self._connection


def create_tables(con: DBConnection) -> None:
    with con.cursor() as cur:
        sql = """
        drop table if exists event;

        CREATE TABLE "event" (
            userId numeric,
            epoch numeric,
            coords Geometry('Point', 4326)    
        )
        """

        cur.execute(sql)


def insert_event(cur, e: Event) -> None:

    sql = """
    insert into event (userId, epoch, coords)
    values (
        %(user_id)s,
        %(epoch)s,
        st_setsrid(st_makepoint( %(lon)s, %(lat)s), %(srid)s)
    )
    """

    cur.execute(
        sql,
        {
            "user_id": e.user_id,
            "epoch": e.timestamp,
            "lon": e.location.lon,
            "lat": e.location.lat,
            "srid": e.location.projection,
        },
    )
