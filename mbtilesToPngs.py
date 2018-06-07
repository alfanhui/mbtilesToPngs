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


def select_all_tiles(conn, tms):
    cur = conn.cursor()
    cur.execute("SELECT * FROM map")

    rows = cur.fetchall()
    assets = {}
    print("Map count: " + str(len(rows)))
    print("TMS: " + str(tms))
    for row in rows:
        image = get_Image(conn, row[3])

        # for printing
        dir = str(row[0]) + "/" + str(row[1])
        assets[dir] = dir

        # tsm check
        xValue = row[2]
        if(tms):
            ymax = 1 << row[0]
            xValue = ymax - row[2] - 1

        # generate png
        blobToFile(
            str(row[0]),  # {z}
            str(row[1]),  # {x}
            str(xValue),  # {y}
            image,  # data
        )
    for asset in assets:
        print ('- assets/map/' + assets[asset] + "/")


def get_Image(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE tile_id = ?", [id])

    row = cur.fetchone()
    return(row[0])


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


def beginConvertion(database, tms):
    # database = "./OSMBright.mbtiles"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Processing mbtiles..\n***********\nIf you find your y coordinates (filename.png) are incorrect, use the -tsm option\n***********\n")
        select_all_tiles(conn, tms)


def main(argv):
    inputDir = ''
    tms = False
    try:
        opts, args = getopt.getopt(argv, "hi:o:tms", ["ifile="])
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
        elif opt in ("-tms"):
            print("-tsm checked")
            tms = True
    if inputDir == '':
        print ('mbtilesToPngs.py -i <path_to_file> (.mbtiles only)')
        sys.exit(2)
    start = time.time()
    beginConvertion(inputDir, tms)
    end = time.time()
    print("Time taken to complete: ", str(round((end - start), 2)), "s")


if __name__ == "__main__":
    main(sys.argv[1:])
