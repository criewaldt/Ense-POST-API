# Ense-POST-API

A 3rd party Python API for uploading to Ense.nyc platform via POST requests.

##How to use

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
ense.Download("https://ense.nyc/ense/13792/orangevioletgreen")

>> Successfully saved: 13792 in /Users/someone/Desktop

```

When you call Ense class, you can include a username as a `STRING` i.e. `ense = Ense("ChrisR")`

Or, you can leave out the username i.e. `ense = Ense()` as default=`"anonymous"`

##Methods

###Upload(filepath, addNameTags, title, unlisted)

This is the method to upload an Ense to Ense.nyc

filepath = `STRING` Path to mp3 file i.e. `"PATH/TO/MP3.mp3"` - default=`None` 

addNameTags = `[STRINGS]` List of nameTags to include i.e. `['foo', 'bar']` - default=`[]`
**NOTE: If you call Ense class with a `username` parameter i.e. `ense = Ense("ChrisR")`, you do not need to include it in `addNameTags`**

title = `STRING` The title of your Ense i.e. `"My Ense!"` - default=`"untitled"` 

unlisted = `BOOLEAN` Wether or not file is listed publicly i.e. `True` - default=`False`

---

###Download(target_url, destination)

This is the method to download an Ense from Ense.nyc

target_url = `STRING` The url of the Ense you want to download i.e. `"https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z"` - default=`None`

destination = `STRING` Desired destination folder for downloaded Ense i.e. `"/Users/someone/Desktop"` - default=`os.path.dirname(os.path.realpath(__file__))`
