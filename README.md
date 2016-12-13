# PyEnse

A 3rd party [Ense](https://www.ense.nyc/) Python SDK

##Requrements
Python 2.7  
Requests  
Requests_toolbelt  

##How to use
Import and call Ense class  
```python
>>> from ense import Ense

>>> ense = Ense(“PyEnse”)
```

Upload an Ense  
```python
>>> ense.Upload("PATH/TO/MP3.mp3", [“SubjectTag1”, “SubjectTag2”, …], “Title goes here!”)

POST 1: 200
POST 2: 204
POST 3: 200
POST 1: 200
POST 2: 200
Ense Url: https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z
```

Download an Ense  
```python
>>> ense.Download("https://ense.nyc/ense/13792/orangevioletgreen", "/Users/someone/Desktop")

Successfully saved: 13792 in /Users/someone/Desktop

```
###`class Ense(username="anonymous")`

- username = `str` The default name tag you want to include in your Ense uploads
i.e. `ense = Ense(“PyEnse”)`

####Methods

####`Upload(filepath=None, addNameTags=[], title="untitled", unlisted=False)`

This is the method to upload an Ense to Ense.nyc

- filepath = `str` Path to mp3 file
i.e. `"PATH/TO/MP3.mp3"`

- addNameTags = `[str, ...]` List of name tags to include
i.e. `['foo', 'bar']`

- title = `str` The title of your Ense
i.e. `"My Ense!"`

- unlisted = `bool` Wether or not file is unlisted publicly
i.e. `False`

---

####`Download(target_url=None, destination=os.path.dirname(os.path.realpath(__file__)))`

This is the method to download an Ense from Ense.nyc

- target_url = `str` The url of the Ense you want to download
i.e. `"https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z"`

- destination = `str` Desired destination folder for downloaded Ense
i.e. `"/Users/someone/Desktop"`

###With help from
[requests_toolbelt](http://toolbelt.readthedocs.io/en/latest/uploading-data.html#streaming-multipart-data-encoder)

[Charles Proxy](https://www.charlesproxy.com/)

StackOverflow [answer](http://stackoverflow.com/questions/12385179/how-to-send-a-multipart-form-data-with-requests-in-python) to my issues with Requests package when passing files parameter for multipart formdata
