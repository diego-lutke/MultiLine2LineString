import psycopg2
from sqlite3 import enable_shared_cache
import os
from dotenv import load_dotenv
from tqdm import tqdm
from shapely import wkt
from pyproj import Geod
from shapely.geometry import LineString

from MultiLine2Line import Multi2Line

def get_pgsql_connection():
        conn = psycopg2.connect(
            host = os.getenv('PGSQL_HOST'),
            database = os.getenv('PUBLIC_TRANSPORT_DATABASE'),
            user = os.getenv('PGSQL_USERNAME'),
            password = os.getenv('PGSQL_PASSWORD')
        )
        return conn

geod = Geod(ellps='WGS84')

# Replace the content of this function with your custom logic to
# load MultiLineStrings from your desired source.
def load_multilinestrings():

    query = [
        "SELECT r.id, ST_ASTEXT(ST_LINEMERGE(ST_COLLECT(w.linestring))) AS geometry",
        "FROM relations r",
        "LEFT JOIN relation_members rm",
        "ON r.id  = rm.relation_id",
        "LEFT JOIN ways w ",
        "ON rm.member_id = w.id",
        "WHERE rm.member_type = 'W'",
        "GROUP BY r.id",
    ]


    with get_pgsql_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(' '.join(query))

            multilinestrings = cursor.fetchall()
    
    return multilinestrings

def transform_multilinestrings(relations):

    failed = []
    linestrings = []
    for i, relation in enumerate(tqdm(relations)):
        transformer = Multi2Line(5)
        multiline = wkt.loads(relation[1])
        if multiline.geom_type == 'MultiLineString':
            line = transformer.run(multiline)
            if len(line) == 1:
                to_insert = f"ST_GEOMFROMTEXT('{line[0].wkt}', 4326)"
            else:
                to_insert = 'NULL'
                failed.append(i)
        else:
            to_insert = f"ST_GEOMFROMTEXT('{relation[1]}', 4326)"
            linestrings.append(i)

        query_update = [
            "UPDATE relations",
            f"SET linestring = {to_insert},",
            f"geometry = ST_GEOMFROMTEXT('{relation[1]}', 4326)"
            f"WHERE id = {relation[0]}"
        ]

        with get_pgsql_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(' '.join(query_update))
            conn.commit()

    return failed, linestrings

if __name__ == '__main__':
    
    print("Transforming MultiLineStrings to LineStrings...")

    multilinestrings = load_multilinestrings()
    failed, linestrings = transform_multilinestrings(multilinestrings)

    print(f"Finished with {len(failed)} failed rows and {len(linestrings)} already LineStrings")