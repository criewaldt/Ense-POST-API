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

When you call Ense(), you can include a username as a `STRING` i.e. `ense = Ense(‘ChrisR’)`

Or, you can leave out the username as `default=‘anonymous’`

##Methods

###Post(filepath, nameTags, title, unlisted)

This is the method to upload an Ense to Ense.nyc

filepath = `STRING` Path to mp3 file i.e. `PATH/TO/MP3.mp3` - `default=None`

nameTags = `[STRINGS]` List of nameTags to include i.e. `['foo', 'bar']` - `default=None`

title = `STRING` The title of your Ense i.e. `My Ense!` - `default='untitled’`

unlisted = `BOOLEAN` Wether or not file is listed publicly i.e. `True’ - `default=False`

###Download(target_url, nameTags, title, unlisted)

This is the method to download an Ense from Ense.nyc

target_url = `STRING` The url of the Ense you want to download i.e. `https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z` `default=None`

destination = `STRING` Desired destination folder for downloaded Ense i.e. `/Users/someone/Desktop` `default=os.path.dirname(os.path.realpath(__file__))`