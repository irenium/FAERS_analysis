#!/usr/bin/python
 
import psycopg2
from config import config


def get_meddra_lists():
    """
    Creates lists of MedDRA preferred terms and 
    their corresponding system organ class.
    """

    f = open('pt.asc', 'r') 
    raw_data = f.readlines()
    f.close()
    
    g = open('soc.asc', 'r')
    raw_soc = g.readlines()
    g.close()
    
    list_of_pt = []
    list_of_codes = []
    list_of_soc = []

    for row in raw_data:
        list_of_codes.append(row[-18:-10])
        list_of_pt.append(row[9:-20])
    
    for code in list_of_codes:  
        for row in raw_soc:
            if code == row[0:8]:
                list_of_soc.append(row[9:].strip())

    return list_of_pt, list_of_soc


def create_tables(pt_list, soc_list):
    """ 
    Create meddra table in PostgreSQL db.
    """

    create_command = (
        """
        CREATE TABLE meddra (
            row_id SERIAL PRIMARY KEY,
            pt VARCHAR(255) NOT NULL,
            soc VARCHAR(255) NOT NULL)
        """)

    conn = None

    try:
        # read database configuration
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # create table
        cur.execute(create_command)

        # execute INSERT statement
        for pt, soc in zip(pt_list, soc_list):
            cur.execute('INSERT INTO meddra (pt, soc) VALUES (%s, %s)', (pt, soc))

        # commit changes to db
        conn.commit()

        # close communication with the PostgreSQL database server
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
 
pt_list, soc_list = get_meddra_lists() 
if __name__ == '__main__':
    create_tables(pt_list, soc_list)
