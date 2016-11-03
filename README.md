# Ense-POST-API

A 3rd party Python API for uploading to Ense.nyc platform via POST requests.

##How to use

Clone repo

Import and call Ense class

```python
from ense import Ense

ense = Ense("ChrisR")
```

Upload an Ense

```python
ense.Upload("PATH/TO/MP3.mp3", ["NameTag1", "NameTag2"...], "Title Goes Here!")

>> POST 1: 200
>> POST 2: 204
>> POST 3: 200
>> POST 1: 200
>> POST 2: 200
>> Ense Url: https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z
```

Download an Ense

```python
ense.Download("https://ense.nyc/ense/13792/orangevioletgreen", "/Users/someone/Desktop")

>> Successfully saved: 13792 in /Users/someone/Desktop

```

##Class Ense(username)

>username = `str` i.e. `ense = Ense("ChrisR")` - default=`"anonymous"`

###Methods

####Upload(filepath, addNameTags, title, unlisted)

>This is the method to upload an mp3 to Ense.nyc

>filepath = `str` Path to mp3 file i.e. `"PATH/TO/MP3.mp3"` - default=`None` 

>addNameTags = `[str, ...]` List of name tags to include i.e. `['foo', 'bar']` - default=`[]`
>>Note: `username` is appended to this list when `Upload` method is called.

>title = `str` The title of your Ense i.e. `"My Ense!"` - default=`"untitled"` 

>unlisted = `bool` Wether or not file is listed publicly i.e. `True` - default=`False`

---

####Download(target_url, destination)

>This is the method to download an Ense from Ense.nyc

>target_url = `str` The url of the Ense you want to download i.e. `"https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z"` - default=`None`

>destination = `str` Desired destination folder for downloaded Ense i.e. `"/Users/someone/Desktop"` - default=`os.path.dirname(os.path.realpath(__file__))`
