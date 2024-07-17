from dynaconf import Dynaconf


class Settings:
    def __init__(self, file_path: str):
        self.settings = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=[file_path],
        )
