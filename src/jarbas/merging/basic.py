def keep(conf, curr, new):
    """
    Always keep the current file (this is a no-op).
    """


def replace(conf, path, data):
    """
    Always replace the current file in path with the new provided data.
    """
    with conf.open_path(path, 'w') as F:
        F.write(data)


#
# Append strategies
#
def append(conf, path, data):
    """
    Append new data to current file.
    """
    with conf.open_path(path, 'a') as F:
        F.write(data)


def append_new_lines(conf, path, data):
    """
    Append new lines
    """


def append_new_lines_commented(conf, path, data, comment=r'#.*'):
    pass



#
# Partial replacement strategies
#
def update_configobj(conf, path, data, keep_old=False):
    pass


def update_ini(conf, path, data, keep_old=False):
    pass


def update_json(conf, path, data, keep_old=False):
    pass


def update_lines_regex(conf, path, data, regex):
    pass