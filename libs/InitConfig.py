import configparser


class InitConfig:

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('./conf/setup.conf')

        # MANDATORY PARAMS.
        try:

            self.host = self.config['PBX']['host']
            self.port = self.config.getint('PBX', 'port')
            self.ssl = self.config.getboolean('PBX', 'ssl')
            self.username = self.config['PBX']['username']
            self.secret = self.config['PBX']['secret']

        except KeyError as ex:
            # Exit the thread if parameters are missing
            print("Critical Params missing from config file under config directory: %s" % ex)
            exit()

        except ValueError as valerr:
            # Exit the thread if there is a value error (like if someone puts a str in a port field)
            print("Parameter invalid. Please input the correct type in the config file: %s" % valerr)
            exit()

        except (configparser.NoSectionError, configparser.NoOptionError) as ex:
            print("Section or option missing from key parameters" % ex)
            exit()


        # OPTIONAL PARAMS.
        try:
            self.providers = self.config.get("PROVIDERS", "sip").split(',')

        except (configparser.NoSectionError, configparser.NoOptionError) as ex:
            # If optionals are missing, do nothing
            pass
