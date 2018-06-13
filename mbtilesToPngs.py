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


def select_all_tiles(conn, tms, databaseName):
    cur = conn.cursor()
    cur.execute("SELECT * FROM map")

    rows = cur.fetchall()
    assets = {}
    print("Map count: " + str(len(rows)))
    print("TMS: " + str(tms))
    for row in rows:
        image = get_image(conn, row[3])

        # for printing
        dir = str(row[0]) + "/" + str(row[1])
        assets[dir] = dir

        # tsm check
        yValue = row[2]
        if(tms):
            ymax = 1 << row[0]
            yValue = ymax - row[2] - 1

        # generate png
        blob_to_file(
            databaseName,
            str(row[0]),  # {z}
            str(row[1]),  # {x}
            str(yValue),  # {y}
            image,  # data
        )
    for asset in assets:
        print ('- assets/map/' + databaseName + '/' + assets[asset] + "/")


def get_image(conn, id):
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


def blob_to_file(dir0, dir1, dir2, dir3, ablob):
    directory = os.path.join(os.path.expanduser('~'),
                             "Desktop", dir0, "map", dir1, dir2)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # mkdir_p("~/Desktop/" + dir0)  # database
    # mkdir_p("~/Desktop/" + dir0 + "/map")  # map
    # mkdir_p("~/Desktop/" + dir0 + "/map/" + dir1 + "/" + dir2)  # zoom
    # mkdir_p("/" + dir0 + "/map/" + dir1 +
    #         "/" + dir2 + "/" + dir3)  # column
    filename = os.path.join(directory, (dir3 + ".png"))
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)


def update_tms_row_to_zxy(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM map")
    rows = cur.fetchall()
    for row in rows:
        ymax = 1 << row[0]
        yValue = ymax - row[2] - 1
        cur.execute("UPDATE map SET tile_row = ? WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?",
                    (yValue, row[0], row[1], row[2]))
        conn.commit()


def begin_convertion(database, tms):
    # create a database connection
    conn = sqlite3.connect(database)
    if database.__contains__("/"):
        database = database.split("/")[-1]
    with conn:
        print("Processing mbtiles..\n***********\nIf you find your y coordinates (filename.png) are incorrect, use the -tsm option\n***********\n")
        select_all_tiles(conn, tms, database.split(".")[0])
        if tms:
            print("Do you want to update the mbtiles database to zxy index?\n(y/n)")
            strInput = input()
            if "y" in strInput:
                update_tms_row_to_zxy(conn)
    conn.close()


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
    begin_convertion(inputDir, tms)
    end = time.time()
    print("Time taken to complete: ", str(round((end - start), 2)), "s")


if __name__ == "__main__":
    main(sys.argv[1:])
