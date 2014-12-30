from pyspeech import best_speech_result
import unittest
from pyaudio import PyAudio
import Queue

class PyspeechTest(unittest.TestCase):
  def setUp(self):
    self.p = PyAudio()

  def test_google_stt(self):
    good_morning = open('example_wavs/good_morning.wav', 'rb')
    output = best_speech_result(self.p, good_morning.read(), {}, "google")
    self.assertEqual(output, "good morning")

    hello_world = open('example_wavs/hello_world.wav', 'rb')
    output = best_speech_result(self.p, hello_world.read(), {}, "google")
    self.assertEqual(output, "hello world")

  # This will fail without a valid wit_token in profile.yml
  def test_wit_stt(self):
    import yaml
    profile = yaml.load(open("profile.yml").read())
    good_morning = open('example_wavs/good_morning.wav', 'rb')
    output = best_speech_result(self.p, good_morning.read(), profile, "wit")
    self.assertEqual(output, "good morning")

    hello_world = open('example_wavs/hello_world.wav', 'rb')
    output = best_speech_result(self.p, hello_world.read(), profile, "wit")
    self.assertEqual(output, "hello world")

if __name__ == "__main__":
  unittest.main()
