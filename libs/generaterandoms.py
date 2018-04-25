import random
import logging
from faker.providers.phone_number.en_US import PhoneNumberProvider
from faker import Generator
from libs.InitConfig import InitConfig

logger = logging.getLogger('phonebooter.libs.generaterandoms')

class GenerateRandoms:

    def __init__(self, CountryCode):

        self.logger = logging.getLogger('phonebooter.generaterandoms.GenerateRandoms')
        self.logger.debug('Creating an instance of GenerateRandoms')
        self.generator = Generator(CountryCode)
        self.generator.seed(random.randrange(1, 99999))
        self.config = InitConfig()

    def phone_number(self):
        """Override the phone number format, or else asterisk will not display caller ID properly."""
        fake = PhoneNumberProvider(generator=self.generator)
        fake.formats = ('###-###-####',
                        '(###)###-####',
                        '1-###-###-####',
                        '###.###.####',
                        '###-###-####',
                        '(###)###-####',
                        '1-###-###-####',
                        '###.###.####')

        return fake.phone_number()

    def provider(self):

        try:

            PROVIDERS = self.config.providers

        except AttributeError as ex:
            # If optional parameter missing, use defaults below
            PROVIDERS = [
                'flowroute',
                'GW1SIPUS',
                'TELNYX'
            ]

        rand = random.SystemRandom()

        return rand.choice(PROVIDERS)
