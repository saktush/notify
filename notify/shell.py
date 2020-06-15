import time


class Shell():

    def __init__(self, alarm_and_db, db, help_path):
        self.help_file = open(help_path, 'r')
        self.alarm_and_db = alarm_and_db
        self.db = db
        self.time_input_needed = False
        self.last_note = 'default'

    @staticmethod
    def time_to_str(datetime):
        struct_time = time.localtime(datetime)
        str_time = time.strftime('%d.%m.%y %H:%M', struct_time)
        return str_time

    @staticmethod
    def time_from_str(str_time):
        struct_time = time.strptime(str_time, '%d.%m.%y %H:%M')
        datetime = int(time.mktime(struct_time))
        return datetime

    def get_new_note_text(self, note_text='default alarm'):
        self.time_input_needed = True
        return note_text

    def get_new_note_time(self, user_time):
        delay = 10
        if not user_time:
            note_time = int(time.time() + delay)
            self.time_input_needed = False
            return note_time
        try:
            note_time = self.time_from_str(user_time)
            self.time_input_needed = False
            return note_time
        except ValueError:
            return 'Set proper time'

    def set_new_note(self):
        if self.alarm_and_db.add_note():
            return 'Note added'
        else:
            return 'Something gone wrong'

    def print_note(self, note):
        return f'{note.id} - {self.time_to_str(note.datetime)} - {note.text}\n'

    def print_all_notes(self):
        notes = self.db.get_notes()
        now = int(time.time())
        output = ''

        output += '\nExpired:\n'
        for note in notes:
            if note.datetime < now:
                output += self.print_note(note)

        output += '\nPlanned:\n'
        for note in notes:
            if note.datetime > now:
                output += self.print_note(note)

        return output

    def process_cmd(self, cmd):

        if cmd.startswith('print'):
            return self.print_all_notes()

        elif cmd.startswith('add'):
            note_text = cmd[4:]
            if not note_text:
                note_text = 'default alarm'

            while True:
                delay = 10
                user_time = input(
                        f'Set time DD.MM.YY HH:MM or Enter for {delay}s:'
                        )
                if not user_time:
                    note_time = int(time.time() + delay)
                    break

                else:
                    try:
                        note_time = self.time_from_str(user_time)
                        break
                    except ValueError:
                        return 'Set proper time'

            if self.alarm_and_db.add_note(note_time, note_text):
                return 'Note added'

        elif cmd.startswith('delete '):
            try:
                note_id = int(cmd[7:])
                if self.alarm_and_db.delete_by_id(note_id):
                    return f'Note {note_id} deleted'
                else:
                    return 'nothing to delete'
            except ValueError:
                return 'Set proper id'

        elif cmd.startswith('h'):
            output = ''
            for line in self.help_file:
                output += line
            return output

        elif cmd.startswith('clear'):
            if self.alarm_and_db.delete_all():
                return 'Cleared all'

        elif cmd.startswith('exit') or cmd == 'x':
            self.help_file.close()
            raise ShellExit

        else:
            return 'Type "h" for help'


class ShellExit(Exception):
    pass


if __name__ == '__main__':
    print('Use main.py to start')
