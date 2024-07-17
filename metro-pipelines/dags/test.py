import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

PIPELINE_NAME = f"test-pipeline"
IMAGE = "0.0.0.0:5000/data-metro:latest"
APPLICATION_ARGS = {
    "GIT_URL": "https://github.com/ali21msh",
    "GIT_ACCESS_TOKEN": "glpat-8PqJMR4hz1wuNCgKcUx2",
    "PIPELINE_PATH": "pipelines/test/test.yml",
    "SETTINGS_PATH": "settings/settings-v1.toml",
    "GIT_REPO_ID": 121,
    "PROFILE": "production",
}

default_args = {
    'owner': 'Ali Mashhadi',
    'depends_on_past': False,
    'start_date': '2024-04-12',
    'email': ['ali_mashhadi78@outlook.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=5)
}

with DAG(
        dag_id=PIPELINE_NAME,
        default_args=default_args,
        schedule="0 1 * * *",
        max_active_runs=1,
        catchup=False,
        concurrency=10
) as dag:
    DockerOperator(
        dag=dag,
        task_id=PIPELINE_NAME,
        image=IMAGE,
        container_name=PIPELINE_NAME + f"-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%s')}",
        api_version="auto",
        auto_remove='force',
        docker_url='unix://var/run/docker.sock',
        network_mode='host',
        tty=True,
        xcom_all=False,
        mount_tmp_dir=False,
        environment=APPLICATION_ARGS
    )
