from typing import Optional

import gitlab
import yaml


# gitlab_repo_url = "https://git.routerhosting.com"
# file_path_in_repo = "path/to/your/file.txt"
# gitlab_access_token = "glpat-GUAtbvckyfy8wqwnuwzw"

class GitHandler:
    repo_url: str
    access_toke: str
    handler: gitlab.Gitlab

    def __init__(self, repo_url: str, repo_id: int, access_token: str):
        self.repo_url = repo_url
        self.access_toke = access_token
        self.handler = gitlab.Gitlab(repo_url, private_token=access_token)
        self.project = self.handler.projects.get(id=repo_id)

    def download_pipeline_file_from_gitlab(self, file_path: str):
        try:
            # Get the raw content of the specified file
            file_content = self.project.files.get(file_path, ref="main").decode()
            return yaml.safe_load(file_content)

        except gitlab.exceptions.GitlabGetError as e:
            print(f"Error downloading file: {e}")
            return None

    def download_settings_file_from_gitlab(self, file_path: str, local_file_path: str) -> Optional[str]:
        try:
            file_content = self.project.files.get(file_path, ref="main").decode()
            with open(local_file_path, 'w+') as file:
                file.write(file_content.decode('UTF-8'))
            return local_file_path
        except Exception as err:
            print(f"Error downloading file: {err}")
            return None

    def parse_repo_id(self):
        return self.repo_url.split("/")[-1]
