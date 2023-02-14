import uuid
import airflow
import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.models import Variable
from kubernetes.client import models as k8s

# resources={
#     'request_cpu': '50m',
#     'request_memory': '150Mi'
# }

affinity = {}

envs = {
}

dag_default_args = {
    'owner': 'etp',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False,
}

dag = DAG(
    'etp_demo_ETL',
    default_args=dag_default_args,
    schedule_interval='30 2 * * *'
)

pod_operator_kwargs = {
    'namespace':'airflow',
    'get_logs': True,
    'dag': dag,
    'is_delete_operator_pod': False,
    'image_pull_policy': 'Always',
    'image_pull_secrets': [k8s.V1LocalObjectReference('regcred')],
    'in_cluster': True,
#     'resources': resources,
    'affinity': affinity,
    'secrets': []
}

#repo names
image_repo = str(Variable.get("DOCKER_URL"))
image_template = image_repo + ":{tag}"

task1 = KubernetesPodOperator(
        image=image_template.format(tag="v1"),
        name="task1",
        task_id="{}-task".format("task1"),
        env_vars={**envs},
        **pod_operator_kwargs)

task1
