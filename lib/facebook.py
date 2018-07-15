import pycurl
from io import BytesIO
from urllib.parse import urlencode

class Facebook(object):
	def __init__(self, data):
		super(Facebook, self).__init__()
		self.email = data['email']
		self.password = data['password']
		self.userAgent = 'NokiaC3-00/5.0 (08.63) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 AppleWebKit/420 (KHTML, like Gecko) Safari/420'
	def login(self):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://m.facebook.com/')
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.COOKIEJAR, 'fbcookie.txt')
		c.setopt(c.COOKIEFILE, 'fbcookie.txt')
		c.setopt(c.USERAGENT, self.userAgent)
		c.perform()
		c.close()
		body = str(buffer.getvalue())
		html = buffer.getvalue()
		#isLogin = True if body.find(loginString) == False else False
		#if isLogin == True:
		if 'name="lsd" value="' in body:
			split1_1 = body.split('name="lsd" value="')
			split1_2 = split1_1[1].split('"')

			split2_1 = body.split('name="m_ts" value="')
			split2_2 = split1_1[1].split('"')

			split3_1 = body.split('name="li" value="')
			split3_2 = split1_1[1].split('"')

			buffer = BytesIO()
			c = pycurl.Curl()
			c.setopt(c.URL, 'https://m.facebook.com/login.php?refsrc=https^%^3A^%^2F^%^2Fm.facebook.com^%^2F^&lwv=100^&refid=8')
			c.setopt(c.WRITEDATA, buffer)
			#c.setopt(c.POST, True)
			c.setopt(c.POSTFIELDS, urlencode({
				'email' : self.email,
				'pass' : self.password,
				'li' : split3_2[0],
				'm_ts' : split2_2[0],
				'lsd' : split1_2[0],
				'login' : 'Masuk',
				'unrecognized_tries' : '0',
				'try_number' : '0'
				}))
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.COOKIEJAR, 'fbcookie.txt')
			c.setopt(c.COOKIEFILE, 'fbcookie.txt')
			c.setopt(c.USERAGENT, self.userAgent)
			c.perform()
			c.close()
			body = buffer.getvalue()
			#print(body.decode('iso-8859-1'))
			return True
		else:
			#print(html.decode('iso-8859-1'))
			return True
	def getFanspageContent(self,fanspageUrlList):
		imageList = []
		for e in fanspageUrlList:
			buffer = BytesIO()
			c = pycurl.Curl()
			c.setopt(c.URL, 'https://m.facebook.com/'+e)
			c.setopt(c.WRITEDATA, buffer)
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.COOKIEJAR, 'fbcookie.txt')
			c.setopt(c.COOKIEFILE, 'fbcookie.txt')
			c.setopt(c.USERAGENT, self.userAgent)
			c.perform()
			c.close()
			body = str(buffer.getvalue())
			'''
			import os
			import webbrowser

			html = body
			path = os.path.abspath('temp.html')
			url = 'file://' + path

			with open(path, 'w') as f:
			    f.write(html)
			webbrowser.open(url)
			'''

			if 'data-ft="&#123;&quot;tn&quot;:&quot;H&quot;&#125;"><div class' in body:
				postSegment = body.split('data-ft="&#123;&quot;tn&quot;:&quot;H&quot;&#125;"><div class')
				for j in range(1,len(postSegment)):
					postSegment3 = {}
					imageList1 = []
					postSegment2 = postSegment[j].split('<div></div><div></div>')
					postSegment2[0] = postSegment2[0].replace('href="/','href="https://m.facebook.com/')
					if 'video_redirect' not in postSegment2[0]:
						imageSegment = postSegment2[0].split('href="')
						for k in range(1,len(imageSegment)):
							imageSegment2 = imageSegment[k].split('"')
							#print('=>>')
							#print(imageSegment2[0])
							#print('\n')
							imageList1.append(imageSegment2[0])
							if(k == 1):
								postSegment3['source'] = imageSegment2[0]
					postSegment3['content'] = imageList1
					imageList.append(postSegment3)
		return imageList

	def getImageURL(self,url):
		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.COOKIEJAR, 'fbcookie.txt')
		c.setopt(c.COOKIEFILE, 'fbcookie.txt')
		c.setopt(c.USERAGENT, self.userAgent)
		c.perform()
		c.close()
		body = str(buffer.getvalue().decode('iso-8859-1'))
		
		if 'View Full Size' in body:
			split_1 = body.split('>View Full Size</a>')
			split_2 = split_1[0].split('href="')
			split_3 = split_2[len(split_2)-1].split('"')
			return split_3[0]
		else:
			return False