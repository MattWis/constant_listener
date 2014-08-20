from thread import start_new_thread
from pyaudio import PyAudio
from pyspeech import listen_for_best_google_speech_result
from time import sleep
import Queue

def background_speech_to_text(queue, duration, interval):
  start_new_thread(_spawn_listeners, (queue, duration, interval, ))

def _spawn_listeners(queue, duration, interval):
  p = PyAudio()
  while True:
    start_new_thread(_listen, (p, queue, duration, ))
    sleep(interval)

def _listen(pyaudio, queue, duration):
  queue.put(listen_for_best_google_speech_result(pyaudio, duration))

if __name__ == "__main__":
  q = Queue.Queue()
  background_speech_to_text(q, 3, 1)

  while True:
    print q.get()

