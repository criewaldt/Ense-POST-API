#!/usr/bin/env python

###for my machine
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
###

import os
import datetime
import requests
import json
from requests_toolbelt import MultipartEncoder

class Ense(object):
    def __init__(self, username="anonymous"):
        self.username = username
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': 'Ense/1 CFNetwork/808.1.4 Darwin/16.1.0'})

    def Download(self, target_url=None, destination=os.path.dirname(os.path.realpath(__file__))):
        if os.path.isdir(destination):
            if target_url and "https://ense.nyc/ense/" in target_url:
                #get key, user values
                results = target_url.split('/')
                user = results[-1]
                key = results[-2]
                #GET: 1
                url = "https://s3.amazonaws.com/media.ense.nyc/enses/" + user + "/" + key + "/0"
                headers = {
                'Origin' : 'https://ense.nyc',
                'Referer' : 'https://ense.nyc/ense/'+key+'/'+user,
                }
                #-get
                r = self.s.get(url, stream=True)
                #save file
                with open(os.path.join(destination, "{}.m4a".format(key)), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                print "Successfully saved: {}".format(key), "in {}".format(destination)
                return
            else:
                print "Error: incorrect URL"
        else:
            print "Error: destination isn't a directory"
        
    
    def Upload(self, mp3_path="", addNameList=[], title="untitled", unlisted=False):
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
            'author':self.username,
            'title':title,
            'mimeType':'audio/mp3',
            'deviceKey':'663mIN8biWie6Kxf1Ctptm',
            'userAgent':'iOSApp',
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
        
        print "Ense Url:", ense_location
        
    
    def _edit(self, addNameList, title, unlisted, dbkey, timestamp):
        #POST: 1
        #create payload for added names
        #add username to payload
        addNameList.append(self.username)
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

if __name__ == "__main__":
    pass
    
