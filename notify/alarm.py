import time
import pyaudio
import wave
import threading


class Alarm(threading.Thread):
    """ this class object are threads of alarmed notes """

    def __init__(self, note_id, datetime, text, audio_path):
        super(Alarm, self).__init__()
        self.note_id = note_id
        self.datetime = datetime
        self.text = text
        self.keeprunning = True
        self.audio_path = audio_path

    def get_id(self):
        return self.note_id

    def make_notification(self):
        self.play_sound(self.audio_path)
        print('Continue\n\nNotification:', self.text, '\nPress ENTER')

    def run(self):
        while self.keeprunning:
            note_time = int(self.datetime)
            now_time = int(time.time())

            if note_time == now_time:
                self.make_notification()
                self.die()
                return True

            elif note_time < now_time:
                self.die()
                return None

            time.sleep(0.5)

    def play_sound(self, filename):
        chunk = 1024
        f = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        data = f.readframes(chunk)

        while data:
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def die(self):
        self.keeprunning = False


if __name__ == '__main__':
    print('Use notify.py to start')
