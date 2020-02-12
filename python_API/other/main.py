import json


def pretty_print_json(input):
    print(json.dumps(input, indent=4, sort_keys=True))

