"""from lib.reddit import *
import json

r = Reddit().getSubRedditPost('dankememes','hot')
s = json.loads(r)
print(s['data']['children'][0])"""
from lib.facebookapi import *
from lib.image import *

fanspageList = [
    'Shitposting2006',
    'InternetTouristGuideII',
    'IhavenomemesImustshitpost',
    'TopDankestMemes',
    'ocfreshstolenmemes1',
    'memesupremeofficial',
]
img = Image()

fb = FacebookAPI({
    'accessToken': 'EAAAAUaZA8jlABAC8mBSprGaBQmFlNDtUFdsf0VBYH28MtlCOYZAgu1E6xFoZAbZBhCaUolXoLGaEfZChKw0SlOgZAHEZC0OTFErrdSCj1AeZAAOX0JrwGlRpO8D2PRMh0O548fwyzwqddOp1gqJkEZCU5mLHLmiCD99yi4r5yWtR4egZDZD'
})
for fanspageIteration in fanspageList:
    fanspageContent = fb.getFanspageContent(fanspageIteration)
    for contentIteration in fanspageContent['data']:
        postData = fb.getImageUrl(contentIteration['id'])
        if len(postData['attachments']['data']) == 1 and postData['attachments']['data'][0]['type'] == 'photo':
            print('ok')
        break
    break
