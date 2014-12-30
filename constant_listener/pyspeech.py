import json
import os
import sys
import wave
import pyaudio
import Queue
import struct
from tempfile import mkstemp
import urllib2
from scikits.samplerate import resample
from scikits.audiolab import Sndfile, Format, wavread
from pocketsphinx import Decoder
from vocabcompiler import compile
from wit import Wit


have_sphinx_dictionary = False
RATE = 16000

def best_speech_result(pyaudio, audio_data, profile, stt_type = "google"):
  wav_name = data_to_wav(pyaudio, audio_data)
  if wav_name == "":
    print("error saving data")
    return ""
  if stt_type == 'google':
    output = best_google_speech_result(pyaudio, wav_name, profile)
  elif stt_type == 'wit':
    output = best_wit_speech_result(pyaudio, wav_name, profile)
  elif stt_type == 'sphinx':
    output = best_sphinx_speech_result(pyaudio, wav_name, profile)

  os.remove(wav_name)
  return output

def best_sphinx_speech_result(pyaudio, wav_name, profile):
  if not have_sphinx_dictionary:
    if not profile.has_key("words"):
      raise "Pass the possible words in in profile"
    compile("sentences.txt", "dictionary.dic", "language_model.lm", profile["words"])
    global have_sphinx_dictionary
    have_sphinx_dictionary = True

  wav_file = file(wav_name, 'rb')
  speechRec = Decoder(
    hmm  = "/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k",
    lm   = "language_model.lm",
    dict = "dictionary.dic"
  )

  speechRec.decode_raw(wav_file)
  results = speechRec.get_hyp()
  return results[0]

def best_google_speech_result(pyaudio, wav_name, profile):
  if not profile.has_key("key") or profile["key"] == '':
    profile["key"] = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
  flac_file = wav_to_flac(wav_name)
  return best_google_result(flac_to_google_result(flac_file, profile["key"]))

def best_wit_speech_result(pyaudio, wav_name, profile):
  if not profile.has_key("wit_token") or profile["wit_token"] == '':
    raise "Pass your Wit API Token in profile"
  w = Wit(profile["wit_token"])
  result = w.post_speech(open(wav_name, 'rb'))
  return result[u'msg_body']

def put_audio_data_in_queue(p, queue):
  CHUNK = 4096

  quiet_time = 0
  current_data = ""

  stream = p.open(input_device_index = None, rate = RATE, channels = 1,
                  frames_per_buffer = CHUNK, format = pyaudio.paInt16,
                  input = True)
  while True:
    data = stream.read(CHUNK)

    # 2 bytes per paInt16
    levels = struct.unpack("%dh"%(len(data)/2), data)

    sum_squares = 0
    for level in levels:
        sum_squares += level * level

    if (sum_squares / CHUNK > 1000000):
      current_data = current_data + data
      quiet_time = 0
    else:
      if (quiet_time > 0.5):               #0.5 second maximum of quietness
        if (len(current_data) / RATE > 1): #0.5 second minimum of loudness
          queue.put(current_data)
        current_data = ""
      quiet_time += (CHUNK + 0.0) / RATE

  stream.stop_stream()
  stream.close()

def data_to_wav(p, audio_data):
  cd, wav_name = mkstemp('tmp.wav')

  wav_file = wave.open(wav_name, 'wb')
  wav_file.setnchannels(1)
  wav_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
  wav_file.setframerate(RATE)
  wav_file.writeframes(audio_data)
  wav_file.close()

  return wav_name

def wav_to_flac(wav_name):
  cd, tmp_name = mkstemp('tmp.flac')

  Signal, fs = wavread(wav_name)[:2]
  assert(fs == RATE)

  fmt = Format('flac', 'pcm16')
  nchannels = 1
  flac_file = Sndfile(tmp_name, 'w', fmt, nchannels, RATE)
  flac_file.write_frames(Signal)

  return tmp_name

def flac_to_google_result(flac_name, key):
  if flac_name == "":
    return ""

  flac_file = open(flac_name, 'rb')

  url = "https://www.google.com/speech-api/v2/recognize"
  url += "?output=json&lang=en-us&key=" + key

  header = {'Content-Type' : 'audio/x-flac; rate=16000'}
  req = urllib2.Request(url, data = flac_file.read(), headers = header)
  result = urllib2.urlopen(req)

  flac_file.close()
  os.remove(flac_name)

  return result.read()

def best_google_result(result):
  if result == "":
    print("No result")
    return ""
  try:
    lines = result.splitlines()
    if "transcript" in lines[0] or len(lines[0]) > 15:
      print("\nFirst line has info:\n" + lines[0] + '\n')
    else:
      return json.loads(lines[1])['result'][0]['alternative'][0]['transcript']
  except:
    return ""

if __name__ == "__main__":
  from thread import start_new_thread
  p = pyaudio.PyAudio()
  audio_data_queue = Queue.Queue()
  start_new_thread(put_audio_data_in_queue, (p, audio_data_queue,))
  while True:
    data = audio_data_queue.get()
    print(len(data))
    print(best_speech_result(p, data, {}, "google"))
