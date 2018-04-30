import os


def get_file_path(filename):
    if not os.path.exists('config'):
        os.makedirs('config')
    return 'config/' + filename
