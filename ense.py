###for my machine
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
###
import datetime
import requests
import json
from requests_toolbelt import MultipartEncoder

class Ense(object):
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'})
    
    def Post(self, mp3_path="", addNameList=[], title="untitled", unlisted=False):
        #open audio file and create mp3 object
        with open(mp3_path, 'rb') as _mp3:
            mp3 = _mp3.read()
            
        #create timestamp and make it uniform to WebApp standard
        timestamp = datetime.datetime.utcnow().isoformat().replace("-","_")
        timestamp = timestamp.replace(":", "_")[:-3]+"Z"
        
        #POST: 1
        url1 = "https://api.ense.nyc/ense/{}".format(timestamp)
        headers = {
            'Host' : 'api.ense.nyc',
            'Origin' : 'https://ense.nyc',
            'Referer' : 'https://ense.nyc/',
            }
        data = {
            'mimeType':'audio/mp3',
            'deviceKey':'qZBxMQvTbhucfDGe2b6s6P',
            'userAgent':'WebApp',
            }
        #-post
        r = self.s.post(url1, headers=headers, data=data)
        #response
        print "POST 1:", r.status_code
        response = json.loads(r.content)
        
        #set vars
        key = response['contents']['uploadKey']
        ### need to change this to grab AccessKeyId from page
        AWSAccessKeyId = 'AKIAJGPMBNUIOKY2WMHA'
        Policy = response['contents']['policyBundle']['policyDoc']
        Signature = response['contents']['policyBundle']['signature']
        dbkey = response['contents']['dbKey']
        
        #POST: 2
        url2 = "https://s3.amazonaws.com/media.ense.nyc/"
        multipart_data = MultipartEncoder(
        fields = (
            ('key', key),
            ('acl', 'public-read'),
            ('AWSAccessKeyId',AWSAccessKeyId),
            ('Policy',Policy),
            ('Signature',Signature),
            ('Content-Type', 'audio/mp3'),
            ('file', ('blob', mp3, 'audio/mpeg'))
            ))
        #-post
        r = self.s.post(url2, data=multipart_data, headers={"Content-Type": multipart_data.content_type,
                                    'Host': 's3.amazonaws.com',
                                    'Origin': 'https://ense.nyc',
                                    'Referer': 'https://ense.nyc/',
                                    })
        print "POST 2:", r.status_code

        #POST 3
        data = {'fileUrl':"https://s3.amazonaws.com/media.ense.nyc/"+key}
        headers = {'Host': 'api.ense.nyc',
                    'Origin': 'https://ense.nyc',
                    'Referer': 'https://ense.nyc/',}
        #-post
        r = self.s.post(url1+'/'+dbkey, headers=headers, data=data)
        print "POST 3:", r.status_code
        
        ense_location = "https://ense.nyc/ense/" + dbkey + '/' + timestamp

        self._edit(addNameList, title, unlisted, dbkey, timestamp)

        print "Ense Url:", ense_location
        
    
    def _edit(self, addNameList, title, unlisted, dbkey, timestamp):
        #POST: 1
        #create payload for added names
        deltas = """{"deltas":[{"RemoveTopic":{"name":"anonymous"}},"""+",".join("""{"UpsertTopic":{"name":"%s"}}""" % n for n in addNameList)+"]}"
        url = "https://api.ense.nyc/topics/{}/{}".format(timestamp, dbkey)
        headers = {
            'Host':'api.ense.nyc',
            'Origin':'https://ense.nyc',
            'Referer':'https://ense.nyc/ense/{}/{}'.format(dbkey, timestamp),
            'content-type':'application/x-www-form-urlencoded;charset=UTF-8',
            }
        data = {
            'deltas':deltas
            }
        r = self.s.post(url, headers=headers, data=data)
        print "POST 1:", r.status_code

        #POST2
        if unlisted:
            flag = 'true'
        else:
            flag = 'false'
        multipart_data = MultipartEncoder(
        fields = (
            ('title', title),
            ('topics', 'undefined'),
            ('humanInterpretation',''),
            ('id',timestamp),
            ('unlisted', flag),))

        #post
        url2 = "https://api.ense.nyc/ense/{}/{}".format(timestamp, dbkey)
        r = self.s.post(url2, data=multipart_data, headers={"Content-Type": multipart_data.content_type,
                                    'Host': 'api.ense.nyc',
                                    'Origin': 'https://ense.nyc',
                                    'Referer':'https://ense.nyc/ense/{}/{}'.format(dbkey, timestamp),
                                    })
        print "POST 2:", r.status_code

    #magic methods
    """
    def __enter__(self):
        #open ense object
        print 'ense'
        return self

    def __exit__(self, type, value, tb):
        #make sure to close everything thats open!
        pass
    """

if __name__ == "__main__":
    ense = Ense()
    ense.Post('mp3/eruption.mp3', ['ChrisR', 'Python API', 'Guitar Solo', 'Van Halen'], "Van Halen: Eruption")
    
