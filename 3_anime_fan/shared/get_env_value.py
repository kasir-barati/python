import os
from django.core.exceptions import ImproperlyConfigured
from shared.read_env import read_env_files


def get_env_value(
        env_variable: str,
        env_file_name: str) -> str:
    try:
        path = os.path.join(os.getcwd(), env_file_name)
        env_value = read_env_files([path])[env_variable]
        return env_value
    except KeyError:
        error_msg = f'Set the {env_variable} environment variable'
        raise ImproperlyConfigured(error_msg)