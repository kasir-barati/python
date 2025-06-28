"""
This method and helper function is temporary
FIXME: get rid of me and do one of the following options:
    1. Dockerize me
    2. Install a 3rd party package which can get multiple env file and is typed
    3. Write that package yourself and publish it
"""
def read_env_files(paths: list[str]) -> dict[str, str]:
    envs: dict[str, str] = {}
    envs_list = [read_env_file(path) for path in paths]

    [envs.update(item) for item in envs_list]
        
    return envs


def read_env_file(path: str) -> dict[str, str]:
    envs: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as env_file:
        lines = env_file.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 0 or line.startswith(('#', ';')):
                continue

            key_value = line.split('=', maxsplit=2)
            envs[key_value[0]] = key_value[1]
    
    return envs
