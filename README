Constant Listener

This repository was created as a utility for a home automation system. It listens in the background, and uses Google's Speech-to-Text API to give the text said through a Queue.

The general usage has it listening for overlapping chunks, so if you read the beginning of this README into the program, the Queue would have in it:
["Constant Listener", "Listener This repository was created", "story was created as a Ute", ...]


Initilization:

Pick your STT engine and follow the instructions there. You pass in a profile argument to background_speech_to_text that is a dictionary containing the relevant credentials.

  Google:
Map 'key' to a valid Google Developer Key.

Follow "Step 1" here: http://progfruits.wordpress.com/2014/05/31/using-google-speech-api-from-python/
(Also, concerns raised in the article are valid.)

If there is no key specified, a default key will be used, which was gotten from https://gist.github.com/alotaiba/1730160. There's a surprising amount of discussion on that page, some of it even useful.

  Sphinx:
If you are using sphinx, you need profile to have "words" mapped to a list of possible outputs.

  Wit.ai:
Map 'wit_token' to a valid wit.ai token. (I use a server token, it will *probably* work with a client token.)

Usage:

To start a listener that triggers every one second and records for 4 seconds (using google STT and default key):

```
q = Queue.Queue()
background_speech_to_text(q, 4, 1, {}, "google")
while True:
  print q.get()
```
