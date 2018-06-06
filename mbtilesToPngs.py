#!/usr/bin/python
import sqlite3
from sqlite3 import Error
import errno
import os
import sys
import getopt
import time


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_images(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM images")

    rows = cur.fetchall()

    print("Image count: " + str(len(rows)))
    for row in rows:
        result = get_Metadata(conn, row[1])
        blobToFile(
            result['zoom'],
            result['column'],
            result['row'],
            row[0],
        )


def get_Metadata(conn, id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM map WHERE tile_id = ?", [id])

    row = cur.fetchone()
    return({'zoom': str(row[0]), 'column': str(row[1]), 'row': str(row[2])})


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def blobToFile(dir0, dir1, dir2, ablob):
    mkdir_p("./" + dir0)  # zoom
    mkdir_p("./" + dir0 + "/" + dir1)  # column
    filename = "./" + dir0 + "/" + dir1 + "/" + dir2 + ".png"
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)


def beginConvertion(database):
    #database = "./OSMBright.mbtiles"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Processing mbtiles..")
        select_all_images(conn)


def main(argv):
    inputDir = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print ('mbtilesToPngs.py -i <path_to_file> (.mbtiles only)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('mbtilesToPngs.py -i <path_to_file> (.mbtiles only)')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputDir = str(arg)
            if not os.path.isfile(inputDir):
                print (inputDir, " file not found")
                sys.exit()
    if inputDir == '':
        print ('mbtilesToPngs.py -i <path_to_file> (.mbtiles only)')
        sys.exit(2)
    start = time.time()
    beginConvertion(inputDir)
    end = time.time()
    print("Time taken to complete: ", str(round((end - start), 2)), "s")


if __name__ == "__main__":
    main(sys.argv[1:])
