import ast
#import json
from lib.database import *
from lib.line import * 

dbcursor.execute("SELECT * FROM cookie")
row = dbcursor.fetchone()
cookie = row['cookie']

line = LINE({
	'cookie' : cookie,
	'id' : '11702069'
})

csrf_token = line.initializePost()

dbcursor.execute("SELECT * FROM post WHERE approval = 'waiting'")
row = dbcursor.fetchone()
w = []
for i in json.loads(row['content']):
	imageData = line.uploadImage({
		'csrf_token' : csrf_token,
		'file' : 'post-assets/'+i,
	})
	w.append(json.loads(imageData))
postData = {
#	'image[1]' : {
#		'id' : '5d1a2657f71a6c18ec717cf5cfa96a15t8841338',
#		'width' : '640',
#		'height' : '572',
#	},
	'text' : 'Source: '+row['source'],
	'csrf_token' : csrf_token,
}
y = 1
for i in w:
	if i == 9:
		break
	postData['image['+str(y)+']'] = {}
	postData['image['+str(y)+']']['id'] = i['media']['objectId']
	postData['image['+str(y)+']']['width'] = i['media']['width']
	postData['image['+str(y)+']']['height'] = i['media']['height']
	y = y+1
post_id = line.post(postData)
dbcursor.execute("UPDATE post SET approval = 'posted', post_id = '"+post_id+"' WHERE id = "+str(row['id']))


"""
p = line.uploadImage({
	'csrf_token' : csrf_token,
	'file' : 'post-assets/',
})
print(p)
{"code":0,"original":"http://dl.os.line.naver.jp/r/myhome/h/fc759802d9b4342e449977effaf62294t883b298","thumb":"http://dl.os.line.naver.jp/r/myhome/h/fc759802d9b4342e449977effaf62294t883b298/m612","media":{"width":800,"obsNamespace":"h","icon":null,"serviceName":"myhome","height":600,"objectId":"fc759802d9b4342e449977effaf62294t883b298","type":"PHOTO","preferCdn":null}}
"""
"""
print(line.post({
	'text' : '',
	'csrf_token' : csrf_token,
}))
{"code":0,"status":200,"error":""}
"""

db.commit()
dbcursor.close()
db.close()