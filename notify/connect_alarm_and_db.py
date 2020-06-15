from notify.alarm import Alarm


class Connect_Alarm_and_DB():
    """ this class connect funclionality of
    DB and Alarm classes so we can add/delete
    notes from db and threads simultaneously.
    You need to add NotificationsDB object first to use"""

    def __init__(self, db, audio_path, setup=True):
        self.db = db
        self.armed_notes = []
        self.audio_path = audio_path
        if setup:
            self.setup()

    def setup(self):
        self.db.create_table()
        self.restore_all_alarms()

    def set_alarm(self, note_id, datetime, text):
        self.armed_notes.append(
                                Alarm(note_id, datetime, text, self.audio_path)
                                )
        self.armed_notes[-1].start()

    def unset_alarm(self, note_id):
        for alarm in self.armed_notes:
            if alarm.get_id() == note_id:
                alarm.die()
                self.armed_notes.remove(alarm)

    def restore_all_alarms(self):
        notes = self.db.get_notes()
        for note in notes:
            self.set_alarm(note.id, note.datetime, note.text)

    def kill_all_alarms(self):
        for alarm in self.armed_notes:
            alarm.die()
            self.armed_notes.remove(alarm)

    """ use the methods below to make changes"""
    def add_note(self, datetime, text):
        note_id = self.db.add_note(datetime, text)
        self.set_alarm(note_id, datetime, text)
        if note_id:
            return True
        else:
            return False

    def delete_by_id(self, note_id):
        self.unset_alarm(note_id)
        if self.db.delete_note(note_id):
            return True
        else:
            return False

    def delete_all(self):
        self.kill_all_alarms()
        if self.db.clear_table():
            return True
        else:
            return False


if __name__ == '__main__':
    print('Use main.py to start')
