import argparse
from libs.phonebooter import PhoneBooter


def main(targetNum, threads, bootLength, wav):

    booter = PhoneBooter()
    booter.launch  (targetNum, threads, bootLength, wav)


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
                        help='Number of async processes to kick off. Default is 2. '
                             '2 is sufficient for cellular devices in most cases.', default=2)
    args = parser.parse_args()

    if args.wav is not None:
        main(args.targetNum, int(args.threads), int(args.bootLength), args.wav)

    else:
        main(args.targetNum, int(args.threads), int(args.bootLength), 'hello-world')
