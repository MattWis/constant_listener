from thread import start_new_thread
from pyaudio import PyAudio
from pyspeech import best_speech_result, put_audio_data_in_queue
from time import sleep
import Queue

def background_stt(queue, profile, stt_type = 'google'):
  start_new_thread(_spawn_listeners, (queue, profile, stt_type,))

def _spawn_listeners(queue, profile, stt_type):
  p = PyAudio()
  audio_data_queue = Queue.Queue()
  start_new_thread(put_audio_data_in_queue, (p, audio_data_queue,))
  while True:
    _listen(p, queue, audio_data_queue, profile, stt_type)

def _listen(pyaudio, queue_out, queue_in, profile, stt_type):
  output = best_speech_result(pyaudio, queue_in.get(), profile, stt_type)
  if output != "":
    queue_out.put(output)

if __name__ == "__main__":
  import yaml
  profile = yaml.load(open("profile.yml").read())
  q = Queue.Queue()
  background_stt(q, profile, 'att')

  while True:
    print(q.get())

