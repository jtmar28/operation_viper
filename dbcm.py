##
#   Group Project:  Weather Processing App
#   Course:         ADEV-3005(234116)
#   Group:          #10
#   Team members:   Justin Martinez, Dean Lorenzo
#   Milestone:      #2
#   Updated:        Apr 5, 2023
#

import sqlite3

class DBCM:
    """Context Manager for SQLite Database Connections and Cursors"""
    def __init__(self, db_name):
        """
        Initializes the DBCM instance with a database name and initializes
        the connection and cursor attributes to None.
        
        Args:
            db_name: The name of the SQLite database file.
        """

        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Opens a connection to the SQLite database and creates a cursor. Returns the
        cursor for use within a with statement.
        
        Returns: The cursor for use within the with statement.
        """

        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Commits the changes made to the database if there were no exceptions, rolls back the
        changes if there was an exception, closes the cursor and connection.
        
        Args:
            exc_type: The type of exception raised, if any.
            exc_val: The value of the exception raised, if any.
            exc_tb: The traceback of the exception raised, if any.
        """

        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.cursor.close()
        self.connection.close()
