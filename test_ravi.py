from airflow import DAG
# from airflow.operators.pod_operator import PodOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    
}

dag = DAG(
    'artifact_registry_example',
    default_args=default_args,
    schedule="@daily",
    catchup=False,
)

# Replace the <PROJECT_ID> and <REGISTRY_ID> placeholder with your own
# values, and specify the name and version of the image in the <IMAGE> placeholder.
# image = "gcr.io/<PROJECT_ID>/<REGISTRY_ID>/<IMAGE>:<TAG>"
image = "us-central1-docker.pkg.dev/airflow-gke-377207/airflow-image-repo/test-repo/test-helloworld-image:v1"


task = KubernetesPodOperator(
    task_id='example_task',
    name='example_pod',
    cmds=["echo", "Hello from Artifact Registry!"],
    image=image,
    namespace='default',
    is_delete_operator_pod=True,
    dag=dag
)
