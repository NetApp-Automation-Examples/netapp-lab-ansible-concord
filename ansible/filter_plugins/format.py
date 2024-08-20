from ansible.errors import AnsibleError, AnsibleFilterError
import sys
from io import StringIO
from unittest.mock import patch

# capture stdout just for this function 
stream = StringIO()

# TODO try to figure out table solution for things like the broadcast 
# domains dicts, which have some values as lists instead of a short strings. It
# does not play nice with print_list_of_dicts_as_table  

def print_list_of_dicts_as_table(list_of_dicts, keys=None):
    if not list_of_dicts: 
        return list_of_dicts

    with patch('sys.stdout', stream):

        # credit: https://stackoverflow.com/a/67198100
        # assuming all dicts have same keys
        first_entry = list_of_dicts[0]
        if keys is None:
            keys = first_entry.keys()
        num_keys = len(keys)

        max_key_lens = [
            max(len(str(item[k])) for item in list_of_dicts) for k in keys
        ]
        for k_idx, k in enumerate(keys):
            max_key_lens[k_idx] = max(max_key_lens[k_idx], len(k))

        fmtstring = ('  '.join(['{{:{:d}}}'] * num_keys)).format(*max_key_lens)

        print(fmtstring.format(*first_entry.keys()))
        print(fmtstring.format(*['-'*key_len for key_len in max_key_lens]))
        for entry in list_of_dicts:
            # handle lists
            row = []
            for cell in entry.values():
                if isinstance(cell, list):
                    cell = ','.join(cell)
                row.append(str(cell))
            print(fmtstring.format(*row))

    return stream.getvalue()

class FilterModule(object):
    def filters(self):
        return {
            'dicts_to_table': print_list_of_dicts_as_table,
        }
