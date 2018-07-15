import urllib.parse
import pycurl
from io import BytesIO
import json

class LINE():
	def __init__(self, data):
		self.cookie = data['cookie']
		if 'id' in data:
			if type(data['id']) == int:
				self.id = str(data['id'])
			else:
				self.id = data['id']
	def initializePost(self):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://admin-official.line.me/'+self.id+'/home/send/')
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.HTTPHEADER, [
			'Cookie: '+self.cookie,
			'Referer: https://admin-official.line.me/',
			'Accept-Language: en-US,en;q=0.9,id;q=0.8,de-DE;q=0.7,de;q=0.6',
			'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
			'Connection: keep-alive',
			'Upgrade-Insecure-Requests: 1'
			])
		c.setopt(c.COOKIEJAR, 'linecookie.txt')
		c.setopt(c.COOKIEFILE, 'linecookie.txt')
		c.setopt(c.ENCODING, 'gzip, deflate')
		c.perform()
		c.close()
		body = str(buffer.getvalue())
		split_1 = body.split('<input type="hidden" name="csrf_token" value="')
		split_2 = split_1[1].split('"')
		try:
			buffer = BytesIO()
			c = pycurl.Curl()
			c.setopt(c.URL, 'https://admin-official.line.me/'+self.id+'/home/api/send_init')
			c.setopt(c.WRITEDATA, buffer)
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.HTTPHEADER, [
				'Cookie: '+self.cookie,
				'Referer: https://admin-official.line.me/',
				'Accept-Language: en-US,en;q=0.9,id;q=0.8,de-DE;q=0.7,de;q=0.6',
				'Accept-Encoding: gzip, deflate, br',
				'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
				'Connection: keep-alive',
				'Accept: */*',
				'Upgrade-Insecure-Requests: 1',
				'X-Requested-With: XMLHttpRequest'
				])
			c.setopt(c.COOKIEJAR, 'linecookie.txt')
			c.setopt(c.COOKIEFILE, 'linecookie.txt')
			c.setopt(c.ENCODING, 'gzip, deflate')
			c.perform()
			c.close()
			return split_2[0]
		except IndexError:
			print('Cookie might be expired')
	def uploadImage(self,data):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://admin-official.line.me/'+self.id+'/home/api/objects')
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.HTTPPOST, [
			('file', (
				c.FORM_FILE, data['file'],
			)),
			('csrf_token', data['csrf_token'])
		])
		c.setopt(c.HTTPHEADER, [
			"Accept: */*",
		    "Accept-Encoding: gzip, deflate, br",
		    "Accept-Language: en-US,en;q=0.9,id;q=0.8,de-DE;q=0.7,de;q=0.6",
		    "Cache-Control: no-cache",
		    "Connection: keep-alive",
		    "Content-Type: multipart/form-data",
		    "Cookie: "+self.cookie,
		    "Origin: https://admin-official.line.me",
		    "Postman-Token: 8b9dc9c8-166a-4c50-93c4-b16ca72d72dc",
		    "Referer: https://admin-official.line.me/11702069/home/send/",
		    "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
			])
		c.setopt(c.COOKIEJAR, 'linecookie.txt')
		c.setopt(c.COOKIEFILE, 'linecookie.txt')
		c.setopt(c.ENCODING, 'gzip, deflate')
		c.perform()
		c.close()
		body = str(buffer.getvalue().decode('utf8'))
		return body
	def post(self, data):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://admin-official.line.me/'+self.id+'/home/api/posts')
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.HTTPHEADER, [
			'Cookie: '+self.cookie,
			'Referer: https://admin-official.line.me/',
			'Accept-Language: en-US,en;q=0.9,id;q=0.8,de-DE;q=0.7,de;q=0.6',
			'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
			'Connection: keep-alive',
			'Upgrade-Insecure-Requests: 1'
			])
		formdata = {
			"csrf_token" : data['csrf_token'],
			"scheduled" : "",
			"tzOffset=-420" : "",
			"sendDate" : "",
			"sendHour" : 0,
			"minutes1" : 0,
			"minutes2" : 0,
			"sendTimetype" : "NOW",
			"contentType1" : "TEXT",
			"body" : data['text'],
			"draftId" : "",
			"contentType2" : "MULTI_IMAGE",
		}
		if 'image[1]' in data:
			formdata["media[1].type"] = "PHOTO"
			formdata["media[1].objectId"] = data['image[1]']['id']
			formdata["media[1].width"] = data['image[1]']['width']
			formdata["media[1].height"] = data['image[1]']['height']
		if 'image[2]' in data:
			formdata["media[2].type"] = "PHOTO"
			formdata["media[2].objectId"] = data['image[2]']['id']
			formdata["media[2].width"] = data['image[2]']['width']
			formdata["media[2].height"] = data['image[2]']['height']
		else:
			formdata["media[2].type"] = "PHOTO"
			formdata["media[2].objectId"] = ""
			formdata["media[2].width"] = ""
			formdata["media[2].height"] = ""
		if 'image[3]' in data:
			formdata["media[3].type"] = "PHOTO"
			formdata["media[3].objectId"] = data['image[3]']['id']
			formdata["media[3].width"] = data['image[3]']['width']
			formdata["media[3].height"] = data['image[3]']['height']
		else:
			formdata["media[3].type"] = "PHOTO"
			formdata["media[3].objectId"] = ""
			formdata["media[3].width"] = ""
			formdata["media[3].height"] = ""
		if 'image[4]' in data:
			formdata["media[4].type"] = "PHOTO"
			formdata["media[4].objectId"] = data['image[4]']['id']
			formdata["media[4].width"] = data['image[4]']['width']
			formdata["media[4].height"] = data['image[4]']['height']
		else:
			formdata["media[4].type"] = "PHOTO"
			formdata["media[4].objectId"] = ""
			formdata["media[4].width"] = ""
			formdata["media[4].height"] = ""
		if 'image[5]' in data:
			formdata["media[5].type"] = "PHOTO"
			formdata["media[5].objectId"] = data['image[5]']['id']
			formdata["media[5].width"] = data['image[5]']['width']
			formdata["media[5].height"] = data['image[5]']['height']
		else:
			formdata["media[5].type"] = "PHOTO"
			formdata["media[5].objectId"] = ""
			formdata["media[5].width"] = ""
			formdata["media[5].height"] = ""
		if 'image[6]' in data:
			formdata["media[6].type"] = "PHOTO"
			formdata["media[6].objectId"] = data['image[6]']['id']
			formdata["media[6].width"] = data['image[6]']['width']
			formdata["media[6].height"] = data['image[6]']['height']
		else:
			formdata["media[6].type"] = "PHOTO"
			formdata["media[6].objectId"] = ""
			formdata["media[6].width"] = ""
			formdata["media[6].height"] = ""
		if 'image[7]' in data:
			formdata["media[7].type"] = "PHOTO"
			formdata["media[7].objectId"] = data['image[7]']['id']
			formdata["media[7].width"] = data['image[7]']['width']
			formdata["media[7].height"] = data['image[7]']['height']
		else:
			formdata["media[7].type"] = "PHOTO"
			formdata["media[7].objectId"] = ""
			formdata["media[7].width"] = ""
			formdata["media[7].height"] = ""
		if 'image[8]' in data:
			formdata["media[8].type"] = "PHOTO"
			formdata["media[8].objectId"] = data['image[8]']['id']
			formdata["media[8].width"] = data['image[8]']['width']
			formdata["media[8].height"] = data['image[8]']['height']
		else:
			formdata["media[8].type"] = "PHOTO"
			formdata["media[8].objectId"] = ""
			formdata["media[8].width"] = ""
			formdata["media[8].height"] = ""
		c.setopt(c.POSTFIELDS, urllib.parse.urlencode(formdata))
		c.setopt(c.COOKIEJAR, 'linecookie.txt')
		c.setopt(c.COOKIEFILE, 'linecookie.txt')
		c.setopt(c.ENCODING, 'gzip, deflate')
		c.perform()
		c.close()
		body = str(buffer.getvalue())
		if '"status":200' in body:
			buffer = BytesIO()
			c = pycurl.Curl()
			c.setopt(c.URL, 'https://admin-official.line.me/'+self.id+'/home/')
			c.setopt(c.WRITEDATA, buffer)
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.HTTPHEADER, [
				'Cookie: '+self.cookie,
				'Referer: https://admin-official.line.me/',
				'Accept-Language: en-US,en;q=0.9,id;q=0.8,de-DE;q=0.7,de;q=0.6',
				'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
				'Connection: keep-alive',
				'Upgrade-Insecure-Requests: 1'
				])
			c.setopt(c.COOKIEJAR, 'linecookie.txt')
			c.setopt(c.COOKIEFILE, 'linecookie.txt')
			c.setopt(c.ENCODING, 'gzip, deflate')
			c.perform()
			c.close()
			body = str(buffer.getvalue())
			return body.split('<a href="./post/')[1].split('/comments"')[0]
		else:
			return False

"""
conf = {
	'cookie' : '__try__=1530482521524;LC=ff6332cde66a668991cbfe6cf26977bc3301aa656ce191013f52dd47349d3cbb;cert=52a42c3d83ace3c512b62dd26d23e91a1f887850ed8eacdf8f700ca7624f0afe;_trmccid=7c16c24ab1214980;X-SCGW-CSRF-Token=ZMWxIuRfDd2bIy1G9nUU7U;',
	'id' : '11702069'
}

t = LINE(conf)

t.post({
	'csrf_token' : t.initializePost()
})
"""