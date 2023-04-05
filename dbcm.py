##
#   Group Project:  Weather Processing App
#   Course:         ADEV-3005(234116)
#   Group:          #10
#   Team members:   Dean Lorenzo, Jesse Kosowan, Justin Martinez
#   Milestone:      #2
#

import logging
import sqlite3 

class DBCM():
    """
    A database context manager which handles setup and teardown code.
    """

    logger = logging.getLogger("main." + __name__)

    def __init__(self, db_name):
        """
        Initializes the database context manager and stores the databases name.
        """
        try:
            self.db_name = db_name
            self.conn = sqlite3.connect(self.db_name)
        except Exception as exception:
            print("DBCM:__init__:", exception)
            self.logger.error("DBCM:__init__:%s", exception)

    def __enter__(self):
        """
        Connects to the database and returns a cursor object.
        """
        try:
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as exception:
            print("DBCM:__enter__:", exception)
            self.logger.error("DBCM:__enter__:%s", exception)
        return None

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Commits changes and closes the connection to the database.
        """
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.cursor.close()
            self.conn.close()
        except Exception as exception:
            print("DBCM:__exit__:", exception)
            self.logger.error("DBCM:__exit__:%s", exception)
