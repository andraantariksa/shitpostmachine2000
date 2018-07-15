from lib.database import *
import time
import datetime
datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
dbcursor.execute("DELETE FROM post WHERE time < DATE_SUB(NOW(), INTERVAL 15 DAY)")

db.commit()
dbcursor.close()
db.close()