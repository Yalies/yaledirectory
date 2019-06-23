import yaledirectory

# "api" name can be whatever is most convenient for your program
api = yaledirectory.YaleDirectory()

from pprint import pprint
res = api.search('Erik')
keys = []
for item in res:
    keys += list(item.keys())
print(list(set(keys)))
