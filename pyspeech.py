import json
import os
import sys
import wave
import pyaudio
from tempfile import mkstemp
import urllib2
from scikits.samplerate import resample
from scikits.audiolab import Sndfile, Format, wavread

from key import key
if key == '':
    raise "Put your Google Developer Key in key.py"

def listen_for_best_google_speech_result(pyaudio, duration):
  return best_result(flac_to_result(wav_to_flac(record_wav(pyaudio, 4))))


def record_wav(p, duration):
  rate = 44100
  cd, wav_name = mkstemp('tmp.wav')

  stream = p.open(rate, 1, pyaudio.paInt16, input = True)
  data = stream.read(rate * duration)
  stream.stop_stream()
  stream.close()

  wav_file = wave.open(wav_name, 'wb')
  wav_file.setnchannels(1)
  wav_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
  wav_file.setframerate(rate)
  wav_file.writeframes(data)
  wav_file.close()

  return wav_name

def wav_to_flac(wav_name):
  cd, tmp_name = mkstemp('tmp.flac')
   
  #Resampling to 16000fs
  rate = 16000.
  Signal, fs = wavread(wav_name)[:2]
  Signal = resample(Signal, rate / float(fs), 'sinc_best')
   
  fmt = Format('flac', 'pcm16')
  nchannels = 1
  flac_file = Sndfile(tmp_name, 'w', fmt, nchannels, rate)
  flac_file.write_frames(Signal)

  os.remove(wav_name)

  return tmp_name

def flac_to_result(flac_name):
  flac_file = open(flac_name, 'rb')

  url = "https://www.google.com/speech-api/v2/recognize"
  url += "?output=json&lang=en-us&key=" + key

  header = {'Content-Type' : 'audio/x-flac; rate=16000'}
  req = urllib2.Request(url, data = flac_file.read(), headers = header)
  result = urllib2.urlopen(req)

  flac_file.close()
  os.remove(flac_name)

  return result.read()
 
def best_result(result):
  try:
    lines = result.splitlines()
    if "transcript" in lines[0] or len(lines[0]) > 15:
      print "\nFirst line has info:\n" + lines[0], '\n'
    else:
      return json.loads(lines[1])['result'][0]['alternative'][0]['transcript']
  except:
    return ""

if __name__ == "__main__":
  p = pyaudio.PyAudio()
  print listen_for_best_google_speech_result(p, 4)

