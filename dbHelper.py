import sqlite3
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from translator import Translator
from mysql.connector import connect, Error
from getpass import getpass


class DBHelper:
    def __init__(self, dbName: str, host: str = None, user: str = None):
        """Constrcutor of the interface between code and db.
            Your SQL password will be asked in terminal for security reasons (if you are not using sqlite).

        Args:
            dbName (str): name of the database (add the ".db" at the end if you are using a sqlite db)
            host (str, optional): hostname (None if you are using sqlite). Defaults to None.
            user (str, optional): username (None if you are using sqlite). Defaults to None.
        """
        if host is None:
            self.__connection = sqlite3.connect(dbName)
            self.__cursor = self.__connection.cursor()
            self.__execute = self.__cursor.execute
        else:
            try:
                self.__connection = connect(
                    host=host,
                    user=user,
                    password=getpass("Enter your password: "),
                    database=dbName
                )
            except Error:
                print("Connection error, the connection to the sql db has failed")
                print("Rerun the code with valids hostname/username/password")
                exit(-1)
            self.__cursor = self.__connection.cursor()
            self.__execute = self.__cursor.execute
        # self.create_test_db()

    def create_test_db(self):
        """Create an example of supported database for SQLITE not SQL
        """
        self.__execute("CREATE TABLE traduction (id INTEGER PRIMARY KEY AUTOINCREMENT, french TEXT, english TEXT, translator TEXT)")
        self.__execute("INSERT INTO traduction (french) VALUES ('Bonjour'), ('traduire c est compliqué'), ('ouais l ordi le fait mieux')")
        self.__execute("COMMIT")

    def get_non_translated(self):
        """Return id and french texts of the not yet translated fiels

        Returns:
            [(int, str)]: list of tuples of id and french text to be translated
        """
        # IF SQL
        if isinstance(self.__connection, MySQLConnection) or isinstance(self.__connection, PooledMySQLConnection):
            self.__execute("SELECT id, french FROM traduction WHERE english IS NULL")
            return self.__cursor.fetchall()
        else:  # ELSE SQLITE
            # note that while converting a mysql db to a sqlite db, the field english becomes the string 'NULL' and not NULL
            # if your empty english fields are set to NULL and not 'NULL' please use the following commented line
            return self.__execute("SELECT id, french FROM traduction WHERE english IS NULL").fetchall()
            # note also that the render of a db way be confusing between 'NULL' and NULL, the best way to see which line has to be use
            # is by printing the length of the returned list, if this is 0 this might mean that you have to use the oter one.
            # return self.__execute("SELECT id, french FROM traduction WHERE english IS 'NULL'").fetchall()

    def set_translation(self, id: int, translatedWord: str, translator: str):
        """Set the field english in db with the translation

        Args:
            id (int): id for which we have to insert the translation
            translatedWord (str): translation
            translator (str): name of the translator
        """
        self.__execute("UPDATE traduction SET english = '{translated}' WHERE id='{ID}'".format(ID=id, translated=translatedWord.replace("'", "''")))
        self.__execute("UPDATE traduction SET translator = '{translatorName}' WHERE id='{ID}'".format(ID=id, translatorName=translator.replace("'", "''")))
        self.__execute("COMMIT")


class useDB():
    def __init__(self, dbHelper: DBHelper, translatorName: str = "Reverso"):
        """Constructor of useDB which is the abstraction that links db and traduction

        Args:
            dbHelper (DBHelper): the db helper that access the database
            translatorName (str, optional): Name of the translator that has to be used. Defaults to "Reverso".
        """
        self.__translator = Translator(translatorName)
        self.__dbHelper = dbHelper

    def set_translator(self, translatorName: str = "Reverso", src="fr", target="en"):
        """Change the translator

        Args:
            translatorName (str, optional): name of the new translator. Defaults to "Reverso".
            src (str, optional): source language. Defaults to "fr".
            target (str, optional): target language. Defaults to "en".
        """
        self.__translator.set_translator(translatorName, src, target)

    def get_supported_languages(self):
        """Print the supported languages for the current translator
        """
        self.__translator.get_supported_languages()

    def translateDB(self):
        """This will fill the empty english fields
        """
        toTranslate = self.__dbHelper.get_non_translated()
        i = 0
        for (id, frenchWord) in toTranslate:
            self.__dbHelper.set_translation(id, self.__translator.translate(frenchWord), self.__translator.getTranslatorName())
            i += 1
            if i % 10 == 0:
                print(f"{i}/{len(toTranslate)}")
