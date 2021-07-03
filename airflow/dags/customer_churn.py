import airflow 
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from helpers.churn import preprocess_churn, train_model


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_path, 'data/Telco/Telco-Customer-Churn.csv')

default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='customer_churn',
    default_args=default_args,
    schedule_interval=None
)

check_csv = GreatExpectationsOperator(
    task_id='validate_csv',
    expectation_suite_name="Telco-Customer-Churn.warning",
    batch_kwargs={
        'path': data_path,
        'datasource': 'Telco__dir',
        'data_context_root_dir': base_path
    },
    dag=dag
)

preproces = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_churn,
    op_kwargs={'data_path': data_path, 'base_path': base_path},
    dag=dag
)

train = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    op_kwargs={'x_path': "{{ti.xcom_pull(task_ids='preprocess_data')[0]}}",
                'y_path': "{{ti.xcom_pull(task_ids='preprocess_data')[1]}}"
    },
    dag=dag
)

check_csv >> preproces >> train
