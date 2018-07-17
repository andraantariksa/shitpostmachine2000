import pycurl
from io import BytesIO
import json

class FacebookAPI:
	def __init__(self,data):
		self.accessToken = data['accessToken']
	def getFanspageContent(self,fanspageId):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://graph.facebook.com/v3.0/' + fanspageId + '/posts?access_token=' + self.accessToken)
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0')
		c.perform()
		c.close()
		body = str(buffer.getvalue().decode('iso-8859-1'))
		return json.loads(body)
	def getImageUrl(self,objectId):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://graph.facebook.com/v3.0/' + objectId + '?fields=attachments&access_token=' + self.accessToken)
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0')
		c.perform()
		c.close()
		body = str(buffer.getvalue().decode('iso-8859-1'))
		return json.loads(body)
	def postImageAsFanspage(self,data):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://graph.facebook.com/v3.0/' + data['fanspageId'] + '/photos?access_token=' + self.accessToken)
		c.setopt(c.POSTFIELDS, urlencode({
			'url' : data['imageUrl'],
			'message' : data['text'],
		}))
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0')
		c.perform()
		c.close()
		body = str(buffer.getvalue().decode('iso-8859-1'))
		return json.loads(body)
		#post_id