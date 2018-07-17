from io import BytesIO
import pycurl

class Reddit:
    def getSubRedditPost(self,subReddit,type='new',sortyBy='new'):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://www.reddit.com/r/'+subReddit+'/'+type+'.json?sort='+sortyBy)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0')
        c.perform()
        c.close()
        return str(buffer.getvalue().decode('iso-8859-1'))