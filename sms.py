import requests
import time
import random
import os
import yaml
import json


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

    x = 0
    number = '17863125175'
    sms = SMSMessenger()
    while x < 20:

        sms.telnyx_sms(number, None)
        time.sleep(1.2)
        x += 1
