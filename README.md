# Ense-POST-API

A 3rd party Python API for uploading to Ense.nyc platform.

##How to use

Clone repository

```python
from ense import Ense

ense = Ense()
ense.Post('PATH/TO/MP3.mp3', ['NameTag1', 'NameTag2'...], "Title Goes Here!")

>> POST 1: 200
>> POST 2: 204
>> POST 3: 200
>> POST 1: 200
>> POST 2: 200
>> Ense Url: https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z
```

##Methods

###Post(filepath, nameTags, title, unlisted)

####This is the main method to post to Ense.nyc

filepath = `STRING` (path to mp3 file, `default=None`)

nameTags = `LIST` of `STRINGS` (i.e. `['foo', 'bar']`, `default=None`)

title = `STRING` (`default='untitled'`)

unlisted = `BOOLEAN` (wether or not file is listed publically, `default=False`)
