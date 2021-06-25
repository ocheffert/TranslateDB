# TranslateDB
Translation in a SQL or sqlite db.


Changing the db system only require to change the implementation of `DBHelper` in `dbHelper.py`.

When the password to connect to a SQL db is asked in terminal, no character is printed while you are typing it for security reasons (as in the Linux terminal).


One can generates a sqlite db example by uncommenting the line `self.create_test_db()` in the constructor of `DBHelper`

All can be run and parametrized from `usage.py`

Using reverso as the translator will slow down ypur code (4x has been observed).


## Structure of expected db:


![structure of db](table.png)


## Used packages:

* sqlite3
* mysql.connector
* getpass
* deep_translator
* reverso_context_api
