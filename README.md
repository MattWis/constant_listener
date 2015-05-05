Constant Listener

This repository was created as a utility for a home automation system. It listens in the background, and uses Speech-to-Text APIs to give the text said through a Queue. The background noise level is calibrated based on the past 30 seconds of data to enable dynamic power thresholding.

Initilization:

Pick your STT engine and follow the instructions there. You pass in a profile argument to background_speech_to_text that is a dictionary containing the relevant credentials.

  Google:
Map 'key' to a valid Google Developer Key.

Follow "Step 1" here: http://progfruits.wordpress.com/2014/05/31/using-google-speech-api-from-python/
(Also, concerns raised in the article are valid.)

If there is no key specified, a default key will be used, which was gotten from https://gist.github.com/alotaiba/1730160. There's a surprising amount of discussion on that page, some of it even useful.

  Sphinx:
If you are using sphinx, you need profile to have "words" mapped to a list of possible outputs. There also may be some additional setup.

Usage:
```
q = Queue.Queue()
background_speech_to_text(q, {}, "google")
while True:
  print q.get()
```
