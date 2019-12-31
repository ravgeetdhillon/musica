import json
import os


def load_data(file_name, directory='data'):
    """
    Loads the data from the specified file.
    """

    with open('{}/{}'.format(directory, file_name), 'r') as f:
        data = json.load(f)

    return data


def save_data(data, file_name, directory='data'):
    """
    Saves the data to the specified file.
    """

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open('{}/{}'.format(directory, file_name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=2)
