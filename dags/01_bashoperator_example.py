'''
    Resources:
    - https://github.com/apache/airflow/blob/main/airflow/operators/bash.py 
    - https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html
    - https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html
    - https://stackoverflow.com/questions/54638295/i-cant-xcom-push-an-arguments-through-bashoperator
    - https://marclamberti.com/blog/airflow-xcom/
'''
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

with DAG(
    dag_id='01_bashoperator_example',
    schedule=None,
    start_date=None,
    catchup=False
) as dag:

    print_pwd = BashOperator(
        task_id = 'print_pwd',
        bash_command = 'echo pwd'
    )

    save_pwd_with_bash = BashOperator(
        task_id = 'save_pwd_with_bash',
        bash_command = 'path=$(pwd);  echo $path > /mnt/e/out/from_bash.txt' # symbol: " ; " allow us to separate commands
    )

    xcom_push = BashOperator(
        task_id = 'xcom_push',
        do_xcom_push = True, # From documentation: If BaseOperator.do_xcom_push is True, the last line written to stdout
         # also be pushed to an XCom when the bash command completes
        bash_command = 'path=$(pwd);  echo $path' # and $path should be saved in XComs with "return_value" key
    )

    xcom_pull = BashOperator(
    task_id="xcom_pull",
    bash_command='echo "{{ ti.xcom_pull(task_ids="xcom_push") }}" >> from_xcom.txt', # you cannot use key of variable because from previous task you can 
    # access only by task id
    cwd = '/mnt/e/out/' # where task should be executed
    )
    
    print_pwd >> [save_pwd_with_bash, xcom_push]
    xcom_push >> xcom_pull