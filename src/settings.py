import json

class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)

try:
    with open("./src/config.json", "r") as config:
        global CONFIG
        CONFIG = obj(json.load(config))
except (PermissionError, FileNotFoundError) as error:
    print(error)
