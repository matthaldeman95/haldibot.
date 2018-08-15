import os
import datetime

def set_reminder(intent, reminder_time, user_id, channel_id):
    message = "<@{}>, you asked me to remind you {}".format(user_id, intent)
    timestring_format = "%b %d %Y %I%M:%S %p"
    timestring_format = "%I:%M %p %B %d %Y"
    timestring = datetime.datetime.strftime(reminder_time, timestring_format)
    command = 'echo "python post.py {} \'{}\'" | at {}'.format(channel_id, message, timestring)
    print(command)
    os.system(command)

if __name__ == "__main__":
    set_reminder("to fix this bot", datetime.datetime.now() + datetime.timedelta(minutes=2))
