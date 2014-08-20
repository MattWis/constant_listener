from thread import start_new_thread
from time import sleep
import Queue

def background_speech_to_text(duration, interval, queue):
    start_new_thread(spawn_listeners, (duration, interval, queue, ))

def spawn_listeners(duration, interval, queue):
    while True:
        start_new_thread(listen, (duration, queue))
        sleep(interval)

def listen(duration, queue):
    print "I'm listening..."
    sleep(duration)
    queue.put("hi")

if __name__ == "__main__":
    q = Queue.Queue()
    background_speech_to_text(4, 1, q)

    while True:
        print q.get()
    


