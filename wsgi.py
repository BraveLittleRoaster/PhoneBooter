import falcon
from web.api import BooterAPI

# API Load
api = application = falcon.API()
booter = BooterAPI()
# Add API path for phone DDoS
api.add_route('/phonedos', booter)
