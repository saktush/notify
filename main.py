import sys
from notify.connect_alarm_and_db import Connect_Alarm_and_DB
from notify.notify_db import NotificationsDB
from notify.shell import Shell, ShellExit


def main():
    db = NotificationsDB('notify/files/storage.db')
    alarm_and_db = Connect_Alarm_and_DB(db, 'notify/files/alarm.wav')
    shell = Shell(alarm_and_db, db, 'notify/files/help.txt')

    print('Hello there!')
    print('Type "h" for help.')

    while True:
        try:
            user_input = input('notify >>> ')
            output = shell.process_cmd(user_input)
            print(output)

        except ShellExit:
            break

    print('Goodbye')
    alarm_and_db.kill_all_alarms()
    sys.exit()


if __name__ == '__main__':
    main()
