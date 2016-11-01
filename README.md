# Ense-POST-API

A 3rd party Python API for uploading audio to Ense.nyc

##How to use
Clone repo

```python
ense = Ense()
ense.Post('PATH/TO/MP3.mp3', ['NameTag1', 'NameTag2'...], "Title Goes Here!")

>> POST 1: 200
>> POST 2: 204
>> POST 3: 200
>> POST 1: 200
>> POST 2: 200
>> Ense Url: https://ense.nyc/ense/13533/2016_11_01T10_39_25.683Z
```
