import yaledirectory
import os

# "api" name can be whatever is most convenient for your program
api = yaledirectory.YaleDirectory(os.environ['YALE_NETID'], os.environ['YALE_PASSWORD'])

from pprint import pprint
results = api.search('George Castillo')
for person in results:
    print(f'{person.display_name} {person.residential_college_name}')
print(api.request('Erik Boesen'))
