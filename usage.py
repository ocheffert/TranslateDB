from dbHelper import DBHelper, useDB


myDBTranslator = useDB(DBHelper("traductionCompleted.db"))
myDBTranslator.translateDB()
