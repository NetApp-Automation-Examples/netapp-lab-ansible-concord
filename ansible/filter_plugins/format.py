from ansible.errors import AnsibleError, AnsibleFilterError
import sys
from io import StringIO
from unittest.mock import patch

stream = StringIO()

# credit: https://stackoverflow.com/a/40389411
def print_list_of_dict_as_table(my_dict, col_list=None, sep='\uFFFA'):
    """ Pretty print a list of dictionaries (my_dict) as a dynamically sized table.
    If column names (col_list) aren't specified, they will show in random order.
    sep: row separator. Ex: sep='\n' on Linux. Default: dummy to not split line.
    Author: Thierry Husson - Use it as you want but don't blame me.
    """
    # snatch the stdout just for this function run
    with patch('sys.stdout', stream):

        if not col_list: col_list = list(my_dict[0].keys() if my_dict else [])
        my_list = [col_list] # 1st row = header
        for item in my_dict: my_list.append([str(item[col] or '') for col in col_list])
        col_size = [max(map(len,(sep.join(col)).split(sep))) for col in zip(*my_list)]
        format_str = ' | '.join(["{{:<{}}}".format(i) for i in col_size])
        line = format_str.replace(' | ','-+-').format(*['-' * i for i in col_size])
        item=my_list.pop(0); line_done=False
        while my_list or any(item):
            if all(not i for i in item):
                item=my_list.pop(0)
                if line and (sep!='\uFFFA' or not line_done): print(line); line_done=True
            row = [i.split(sep,1) for i in item]
            print(format_str.format(*[i[0] for i in row]))
            item = [i[1] if len(i)>1 else '' for i in row]
    
    # return the stdout 
    return stream.getvalue()

class FilterModule(object):
    def filters(self):
        return {
            'dicts_to_table': print_list_of_dict_as_table,
        }
