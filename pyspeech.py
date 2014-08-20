import sys
from tempfile import mkstemp
import urllib2
from scikits.samplerate import resample
from scikits.audiolab import Sndfile, Format, wavread
 
if len(sys.argv) < 2 :
    print 'Usage: %s <audio file.wav>' %sys.argv[0]
    sys.exit(0)

wav = sys.argv[1]

def wav_to_flac(wav_name):
    cd, tmp_name = mkstemp('TmpSpeechFile.flac')
     
    #Resampling to 16000fs
    rate = 16000.
    Signal, fs = wavread(wav_name)[:2]
    Signal = resample(Signal, rate / float(fs), 'sinc_best')
     
    # Create the flac file
    fmt = Format('flac', 'pcm16')
    nchannels = 1
    flac_file = Sndfile(tmp_name, 'w', fmt, nchannels, rate)
    flac_file.write_frames(Signal)

    return tmp_name

def flac_to_result(flac_name):
    flac_file = open(flac_name, 'rb').read()
    url = "https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyD6Cba8xQZUMnw_FUEaeJOTOz-kBMIf6l4"
    header = {'Content-Type' : 'audio/x-flac; rate=16000'}
    req = urllib2.Request(url, data = flac_file, headers = header)
    return urllib2.urlopen(req)
 
#Sending to google the file .flac
result = flac_to_result(wav_to_flac(wav))
print result.read()
