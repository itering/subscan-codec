import json
import os


def load_type_registry(name):
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, '{}.json'.format(name))

    if os.path.exists(os.path.abspath(path)) is False:
        return

    with open(os.path.abspath(path), 'r') as fp:
        data = fp.read()
    data = json.loads(data)
    if "default" not in data:
        data = {'default': convert_type_registry(name)}
    return data


def convert_type_registry(name):
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, '{}.json'.format(name))

    with open(os.path.abspath(path), 'r') as fp:
        data = fp.read()
    type_registry = json.loads(data)

    convert_dict = dict()

    for type_string, type_struct in type_registry.items():
        if type(type_struct) == dict:
            if '_enum' in type_struct:
                convert_dict[type_string] = {
                    "type": "enum",
                    "type_mapping": try_struct_convert(type_struct["_enum"])
                }
            elif '_struct' in type_struct:
                convert_dict[type_string] = type_struct["_struct"]
            else:
                convert_dict[type_string] = {
                    "type": "struct",
                    "type_mapping": try_struct_convert(type_struct)
                }
        else:
            convert_dict[type_string] = type_struct
    return convert_dict


def try_struct_convert(struct):
    n = []
    for type_string, type_struct in struct.items():
        if type_struct is None:
            type_struct = "null"
        n.append([type_string, type_struct])
    return n
