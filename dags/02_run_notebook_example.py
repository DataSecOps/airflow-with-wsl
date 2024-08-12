from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator

# https://stackoverflow.com/questions/67811531/how-can-i-execute-a-ipynb-notebook-file-in-a-python-script
def run_notebook_as_script(notebook_path):
    import json
    with open(notebook_path) as fp:
        nb = json.load(fp)
        print(f"Script {notebook_path} loaded into JSON successfully.")
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(line for line in cell['source'] if not line.startswith('%'))
            exec(source)

# example implementation of using notebook
def _run_notebook():
    run_notebook_as_script('/mnt/e/airflow-with-wsl/notebooks/01_names.ipynb') # you must adjust paths

def _import_raw():
    import pandas as pd 
    # read raw directly from web
    df_man = pd.read_csv('https://api.dane.gov.pl/media/resources/20240126/3-Wykaz_imion_m%C4%99skich_nadanych_dzieciom_urodzonym_w_2023_r._wg_pola_imi%C4%99_pierwsze__statystyka_og%C3%B3lna_dla_ca%C5%82ej_Polski.csv')
    df_fem = pd.read_csv('https://api.dane.gov.pl/media/resources/20240126/3-Wykaz_imion_%C5%BCe%C5%84skich_nadanych_dzieciom_urodzonym_w_2023_r._wg_pola_imi%C4%99_pierwsze__statystyka_og%C3%B3lna_dla_ca%C5%82ej_Polski.csv')

    # save to data directory
    df_man.to_csv('/mnt/e/airflow-with-wsl/data/males_name_2023.csv', header=True, index=False)  # you must adjust paths
    df_fem.to_csv('/mnt/e/airflow-with-wsl/data/females_name_2023.csv', header=True, index=False) # you must adjust paths

with DAG (
    dag_id='02_run_notebook',
    schedule=None,
    start_date=None,
    catchup=False
) as dag:
    clean_old_raw = BashOperator(
        task_id = 'clean_old_raw',
        bash_command = 'rm -f $AIRFLOW_HOME/data/males_name_2023.csv $AIRFLOW_HOME/data/females_name_2023.csv'
    )
    import_raw = PythonOperator(
        task_id = 'import_raw_data',
        python_callable=_import_raw,
    )
    run_notebook = PythonOperator(
        task_id = 'run_notebook',
        python_callable=_run_notebook,
    )
    clean_old_raw >> import_raw >> run_notebook