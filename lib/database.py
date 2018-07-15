import mysql.connector
from mysql.connector import errorcode

try:
	db = mysql.connector.connect(user='root', password='@ndra123', database='shitpostmachine2000',buffered=True)
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
dbcursor = db.cursor(dictionary=True)
#else:
#  db.close()