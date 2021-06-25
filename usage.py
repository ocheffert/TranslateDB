from dbHelper import DBHelper, useDB


# myDBTranslator = useDB(DBHelper("traductionCompleted.db"))  # for sqlite
myDBTranslator = useDB(DBHelper(dbName="test", host="localhost", user="root"))  # for sql

"""
If you want to change the translator, consider:

>>> myDBTranslator = useDB(DBHelper(dbName="test", host="localhost", user="root"), translatorName="Google)

REVERSO IS USED BY DEFAULT BUT IS SLOWER AND CANNOT HANDLE TOO MUCH WORDS IN A SAME STRING /!\
In this case, the code will detect the failure of reverso and ask to Google translate to do the job
But if you know that you have long strings, sentences or you hate waiting, use GoogleTranslate or MyMemory
"""

myDBTranslator.translateDB()
