import yaledirectory

# "api" name can be whatever is most convenient for your program
api = yaledirectory.YaleDirectory()

from pprint import pprint
pprint(api.search('Erik'))
