import yaledirectory
import os

# "api" name can be whatever is most convenient for your program
api = yaledirectory.YaleDirectory(os.environ['YALE_API_KEY'])

from pprint import pprint
pprint(api.search('Erik'))
