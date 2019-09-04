import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List


def lazy_format(format_this, *args, **kwargs):
    """loose implementation of string.format().
    performs replacements without enforcing keys existence
    (i.e. replace what you can, do not raise an exception on
    missing key)"""

    if args:
        for idx, val in enumerate(args):
            format_this = format_this.replace(
                "{" + str(idx) + "}", str(val))

    pattern = re.compile(".*?(\{.*?\}).*?")
    formatted = format_this
    to_replace = [item for item in re.findall(pattern, format_this)]
    for item in to_replace:
        if kwargs.get(item[1:-1]) is not None:
            formatted = formatted.replace(item, str(kwargs.get(item[1:-1])))
    return formatted


def get_dict_from_file(file_path: str) -> dict:
    """
    gets a path to json file and return it as a dict
    """
    with open(file_path) as json_file:
        file_data = json_file.read()
        json_dict = json.loads(file_data)

    return json_dict


def recursive_format(format_this, *args, **kwargs):
    """recursively format string, list, dict or tuple.
    note: any other type of object is returned as-is"""

    if isinstance(format_this, str):
        res = lazy_format(format_this, *args, **kwargs)
    elif isinstance(format_this, list):
        res = [recursive_format(item, *args, **kwargs)
               for item in format_this]
    elif isinstance(format_this, tuple):
        res = tuple(recursive_format(item, *args, **kwargs)
                    for item in format_this)
    elif isinstance(format_this, dict):
        res = {}
        for key, val in format_this.items():
            res[key] = recursive_format(val, *args, **kwargs)
    else:
        res = format_this

    return res


def stringify(string_this):
    """recursively convert string_this to str(s).
    note: this function works differently """

    if isinstance(string_this, str):
        return string_this
    elif isinstance(string_this, dict):
        return {str(key): stringify(val) for key, val in string_this.items()}
    elif isinstance(string_this, list):
        return [stringify(item) for item in string_this]
    elif isinstance(string_this, tuple):
        return tuple(stringify(item) for item in string_this)
    elif isinstance(string_this, set):
        return set(stringify(item) for item in string_this)
    else:
        return str(string_this)


def generate_unique_id(obj_type: str):
    # making sure no unique_id is generated twice
    time.sleep(0.000001)
    unique_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if obj_type.lower() == "file":
        return f"f-{unique_id}"
    elif obj_type.lower() == "message":
        return f"m-{unique_id}"
    else:
        return unique_id


def datetime_from_string(string_date,
                         date_format="%Y-%m-%dT%H:%M:%S"):
    return datetime.strptime(string_date, date_format)


def bind(port):
    """
    Binds to specified port
    This can be used to run single instance of a process
    :param port: port number to bind to
    :return: socket. If port can't be bound - returns None
    """

    global socketHold
    try:
        import socket
        socketHold = socket.socket()
        host = socket.gethostname()
        socketHold.bind((host, port))
        return True
    except Exception:
        return False


def rename_file_with_suffix(original_file_path: Path, suffix: str) -> Path:
    """
    Adds a string suffix to the file's name and returns a Path object of thekj
    new file
    :param original_file_path: Path object of the file to rename
    :param suffix:
    :return:
    """
    file_folder = original_file_path.parent
    # if there is a dot (".") in the file name - last one is for the extension
    file_parts = original_file_path.name.split(".")
    file_name = "".join(file_parts[:-1])
    file_extension = file_parts[-1]

    new_file_name = file_name + suffix

    new_file_path = \
        Path(file_folder) / f"{new_file_name}.{file_extension}"

    return new_file_path


def sort_list_of_dicts_by_dict_key(list_to_order: List[dict],
                                   dict_key: str,
                                   custom_order: dict = None) -> List[dict]:
    """
    Sorts a list of dicts according to a specific key in the dicts.
    It can be by the value of that key in the dicts themsleves
    (e.g. alphabetic) or by the value of that key in a custom_order dict.
    :param list_to_order: List of dicts, to sort by a specific key
    :param dict_key: The key in the dicts, if custom_order is NONE,
                        else it is the key in the custom_order
    :param custom_order: Dict with custom order for the list_to_order,
                            to be sorted by.
    :return: sorted list of dicts
    """
    if custom_order:
        ordered_list = sorted(list_to_order,
                              key=lambda x: custom_order[x[dict_key]])
    else:
        ordered_list = sorted(list_to_order,
                              key=lambda x: x[dict_key])
    return ordered_list


def get_sql_string_from_file(file_name: str, path_config: dict) -> str:
    """
    Receives a name of the sql file and returns the sql_string inside
    the file.
    :param file_name: name of the file with the sql query
    :param path_config: dict from the config.ini with path to sql_scripts
                        folder and file_name
    :return: string of the sql query
    """
    try:
        sql_scripts_folder = path_config["sql_scripts"]
        dropdowns_query_file = path_config[file_name]

        sql_path = Path(sql_scripts_folder) / dropdowns_query_file

        with sql_path.open() as fil:
            sql_query = fil.read()

        return sql_query

    except Exception:
        # TODO: add log handling
        raise
