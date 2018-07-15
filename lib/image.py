import pycurl
from io import BytesIO
import magic
import hashlib

class Image():
	def getImage(self,url):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		#c.setopt(c.COOKIEJAR, 'fbcookie.txt')
		#c.setopt(c.COOKIEFILE, 'fbcookie.txt')
		#c.setopt(c.USERAGENT, self.userAgent)
		c.perform()
		c.close()
		body = str(buffer.getvalue())
		return body

	def getImageMIME(self,fname):
		mime = magic.Magic(mime=True)
		t = mime.from_file('post-assets/'+fname)
		if "image" in t:
			return t.replace('image/','')
		else:
			return False

	def saveImage(self,fname,url):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.perform()
		c.close()
		body = buffer.getvalue()
		f = open('post-assets/'+fname,'wb')
		f.write(body)
		f.close()

	def md5Check(self,fname):
		hash_md5 = hashlib.md5()
		with open('post-assets/'+fname, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return hash_md5.hexdigest()