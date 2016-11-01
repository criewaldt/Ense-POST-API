import sys, base64, json
sys.path.append("/usr/local/lib/python2.7/site-packages")
import requests
f = open('pony.mp3', 'rb')
#AudioBinary = base64.b64encode(f.read())
AudioBinary = f.read()
from requests_toolbelt import MultipartEncoder
f.close()

timestamp = "2016_10_22T00_46_43.616Z"
with requests.Session() as s:
    #POST 1
    init_url = "https://api.ense.nyc/ense/{}".format(timestamp)
    headers = {
        'Host' : 'api.ense.nyc',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Origin' : 'https://ense.nyc',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer' : 'https://ense.nyc/',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
            }
    data = {
        'mimeType':'audio/mp3',
        'deviceKey':'qZBxMQvTbhucfDGe2b6s6P',
        'userAgent':'WebApp',
        }
    #post
    r = s.post(init_url, headers=headers, data=data)
    #response
    response = json.loads(r.content)

    key = response['contents']['uploadKey']
    AWSAccessKeyId = 'AKIAJGPMBNUIOKY2WMHA'
    Policy = response['contents']['policyBundle']['policyDoc']
    Signature = response['contents']['policyBundle']['signature']
    dbkey = response['contents']['dbKey']


    #POST 2
    mp3_url = "https://s3.amazonaws.com/media.ense.nyc/"
    multipart_data = MultipartEncoder(
    fields = (
        ('key', key),
        ('acl', 'public-read'),
        ('AWSAccessKeyId',AWSAccessKeyId),
        ('Policy',Policy),
        ('Signature',Signature),
        ('Content-Type', 'audio/mp3'),
        ('file', ('blob', AudioBinary, 'audio/mpeg'))
        
        
        ))

    #post
    r = s.post(mp3_url, data=multipart_data, headers={"Content-Type": multipart_data.content_type,
                                'Host': 's3.amazonaws.com',
                                'Origin': 'https://ense.nyc',
                                'Referer': 'https://ense.nyc/',
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                                })
    #response
    response = r.content

    #POST 3
    
    dest = key.split('enses/')[1]
    
    upload_url = "https://api.ense.nyc/ense/" + dest
    data = {'fileUrl':"https://s3.amazonaws.com/media.ense.nyc/"+key}
    headers = {'Host': 'api.ense.nyc',
                'Origin': 'https://ense.nyc',
                'Referer': 'https://ense.nyc/',}

    r = s.post(init_url, headers=headers, data=data)

    ense_location = "https://ense.nyc/ense/" + dbkey + '/' + timestamp

    print ense_location

