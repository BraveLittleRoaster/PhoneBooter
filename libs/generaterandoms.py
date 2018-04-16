import random
import logging
from faker.providers.phone_number.en_US import PhoneNumberProvider
from faker import Generator

logger = logging.getLogger('phonebooter.libs.generaterandoms')

class GenerateRandoms:

    def __init__(self, CountryCode):

        self.logger = logging.getLogger('phonebooter.generaterandoms.GenerateRandoms')
        self.logger.debug('Creating an instance of GenerateRandoms')
        self.generator = Generator()
        self.generator.seed(random.randrange(1, 99999))

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
