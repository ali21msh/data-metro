import os


class EnvParser:
    env_var_names = ['GIT_URL', 'GIT_ACCESS_TOKEN', 'GIT_REPO_ID', 'PIPELINE_PATH', 'PROFILE','SETTINGS_PATH']
    env_vars: dict

    def __init__(self):
        self.env_vars = {}
        for var in self.env_var_names:
            self.env_vars[var] = os.getenv(var)
