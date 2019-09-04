import configparser
import pathlib


ENV_SETTINGS_NAMING_TEMPLATE = 'config.ini'


def get_environment_settings_path(
        working_path, naming_template=ENV_SETTINGS_NAMING_TEMPLATE):
    """when working_path is a file, all settings will be read from it,
    when working_path is a dir, settings are read from the CLOSEST
    file that matches naming_pattern - up the tree"""

    try:
        current_path = pathlib.Path(str(working_path))
    except Exception:
        raise Exception(
            'invalid environment settings path: ' + str(working_path))

    if current_path.is_file():
        return current_path

    elif current_path.is_dir():
        # search for closest file that matches the naming pattern
        search_path = [current_path] + [pathlib.Path(dir_)
                                        for dir_ in current_path.parents]

        for dir_ in search_path:
            matching_files = [file for file in dir_.glob(naming_template)]
            if matching_files:
                return matching_files[0]
        else:
            return None

    else:
        return None


def get_environment_settings(working_path,
                             naming_template=ENV_SETTINGS_NAMING_TEMPLATE,
                             filter_result=None):
    """"get environment settings from file into dict.
    filter_result should be a dict of requested sections and options.
    example:
    {"section1": ["option1", "option2", ..., "optionN"]}
    """

    env_path = get_environment_settings_path(working_path, naming_template)
    assert env_path, 'invalid environment settings path: ' + str(working_path)

    config_ = configparser.ConfigParser()
    config_._interpolation = configparser.ExtendedInterpolation()
    config_.read(env_path.as_posix())

    if filter_result:
        return {section: {option: config_.get(section, option)
                          for option in filter_result.get(section) or
                          config_.options(section)}
                for section in
                [s_ for s_ in filter_result if s_ in config_.sections()]}

    else:
        return {section: {option: config_.get(section, option)
                          for option in config_.options(section)}
                for section in config_.sections()}
