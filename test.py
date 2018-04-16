from libs.generaterandoms import GenerateRandoms
from asterisk.ami import AMIClient, AMIClientAdapter



def main(targetNum):

    random_number = GenerateRandoms('en_US').phone_number()
    client = AMIClient(address='127.0.0.1',port=5038)
    client.login(username='test',secret='password')

    adapter = AMIClientAdapter(client)
    adapter.Originate(
        Channel='SIP/flowroute/{num}'.format(num=targetNum),
        CallerID='{idnum}'.format(idnum=random_number),
    )