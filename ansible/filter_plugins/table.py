from ansible.errors import AnsibleError, AnsibleFilterError

# credit: https://stackoverflow.com/a/40389411
def print_list_of_dict_as_table(my_dict, col_list=None, sep='\uFFFA'):
    """ Pretty print a list of dictionaries (my_dict) as a dynamically sized table.
    If column names (col_list) aren't specified, they will show in random order.
    sep: row separator. Ex: sep='\n' on Linux. Default: dummy to not split line.
    Author: Thierry Husson - Use it as you want but don't blame me.
    """
    if not col_list: col_list = list(my_dict[0].keys() if my_dict else [])
    my_list = [col_list] # 1st row = header
    for item in my_dict: my_list.append([str(item[col] or '') for col in col_list])
    colSize = [max(map(len,(sep.join(col)).split(sep))) for col in zip(*my_list)]
    formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
    line = formatStr.replace(' | ','-+-').format(*['-' * i for i in colSize])
    item=my_list.pop(0); lineDone=False
    while my_list or any(item):
        if all(not i for i in item):
            item=my_list.pop(0)
            if line and (sep!='\uFFFA' or not lineDone): print(line); lineDone=True
        row = [i.split(sep,1) for i in item]
        print(formatStr.format(*[i[0] for i in row]))
        item = [i[1] if len(i)>1 else '' for i in row]

class FilterModule(object):
    def filters(self):
        return {
            'dicts_to_table': print_list_of_dict_as_table,
        }
