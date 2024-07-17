import yaml

from config.settings import Settings
from utils.env_parser import EnvParser
from utils.git_handler import GitHandler
from utils.navigator import Navigator


def main():
    env_parser = EnvParser()
    print(env_parser.env_vars)
    profile = env_parser.env_vars.get('PROFILE')
    if profile and profile == 'development':
        with open(env_parser.env_vars['PIPELINE_PATH'], 'r') as file:
            pipeline = yaml.safe_load(file)
        settings = Settings(file_path=env_parser.env_vars['SETTINGS_PATH'])
    else:
        file_handler = GitHandler(
            repo_url=env_parser.env_vars['GIT_URL'],
            repo_id=env_parser.env_vars['GIT_REPO_ID'],
            access_token=env_parser.env_vars['GIT_ACCESS_TOKEN'])
        pipeline = file_handler.download_pipeline_file_from_gitlab(file_path=env_parser.env_vars['PIPELINE_PATH'])
        if not pipeline:
            raise Exception("Pipeline File Not Found")
        settings_file_path = file_handler.download_settings_file_from_gitlab(env_parser.env_vars['SETTINGS_PATH'],
                                                                             'settings.toml')
        if not settings_file_path:
            raise Exception("Settings File Not Found")
        settings = Settings(file_path=settings_file_path)
    nav = Navigator(pipeline, settings)

    nav.navigate()


if __name__ == '__main__':
    main()
