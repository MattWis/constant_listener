from thread import start_new_thread
from pyaudio import PyAudio
from pyspeech import listen_for_best_speech_result
from time import sleep
import Queue

def background_stt(queue, duration, interval, profile, stt_type = 'google'):
  start_new_thread(_spawn_listeners, (queue, duration, interval, profile, stt_type, ))

def _spawn_listeners(queue, duration, interval, profile, stt_type):
  p = PyAudio()
  while True:
    start_new_thread(_listen, (p, queue, duration, profile, stt_type, ))
    sleep(interval)

def _listen(pyaudio, queue, duration, profile, stt_type):
  queue.put(listen_for_best_speech_result(pyaudio, duration, profile, stt_type))

if __name__ == "__main__":
  import yaml
  profile = yaml.load(open("profile.yml").read())
  q = Queue.Queue()
  background_stt(q, 4, 2, profile, "google")

  while True:
    print(q.get())

