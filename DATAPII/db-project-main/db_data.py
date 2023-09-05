import pandas as pd
import psycopg2
from fill_website_field import fill_site

# Database connection parameters
db_params = {
    'database': 'DEP',
    'user': 'postgres',
    'password': '',
    'host': 'vichogent.be',
    'port': '40045',
    'options': '-c search_path=dep'
}

def insert_query(query, comp, id, text, url):
    try:
        print("Connecting to the database")
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        print("Executing the query")
        
        cur.execute(query, (comp, url, text, id))
        conn.commit()
    except (Exception) as error:
        print(f"PostgreSQL error: {error}")
    finally:
        cur.close()
        conn.close()

def get_onderneming(limit=4000):
    query = """
        SELECT * FROM dep."Onderneming"
        WHERE "ID" NOT IN (SELECT id FROM dep."html_paginas")
        AND "WebAdres" IS NOT NULL
        LIMIT %s
    """
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute(query, (limit,))
        result = cur.fetchall()
        return result
    except (Exception) as error:
        print(f"PostgreSQL error: {error}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    ondernemingen = get_onderneming()
    print(f"Number of ondernemingen: {len(ondernemingen)}")

    
    
	                                                        
                                                    


