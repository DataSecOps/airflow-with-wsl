# Airflow Installation - Commands

## Linux

### Update sudo apt (Debian-based Linuxes)
In Linux terminal after installation of WSL on your Windows machine
```sh
sudo apt update
sudo apt upgrade
```

### Installation of necessary tools on WSL
```sh
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
```
and after that we can create a virtual environment for Python `python3 -m venv airflow_env` in your $HOME directory

## Apache Airflow

### Installation of Airflow
To avoid problem of dependency you should activate Python virtual environment dedicated for Apache Airflow:
`source airflow_env/bin/activate`
and then you should go to destination where you want to keep Airflow project data (probably some git repo on Windows File System) so for example:
```
cd /mnt/<drive>/<path>/<like>/<in>/<Windows>

for example: /mnt/e/airflow-with-wsl
```
where `mnt` is some kind of "prefix" which allow you to access data on Windows File System from your WSL.

### AIRFLOW_HOME setup
You have to establish this AIRFLOW_HOME in your bash configuration file. The directory set as this variable should be the path you have chosen in above step. To access this configuration file you must be on your $HOME directory and then type
`vim ~/.bashrc` you can of course use other text editor, like nano.

In the few first lines you should add the following code (adjusted to your path)
`export AIRFLOW_HOME =/mnt/e/airflow-with-wsl`

After this a bashrc should be reloaded with `source ~/.bashrc` and after that you might need to rerun your virtual env.

To check if the value is properly set: `echo $AIRFLOW_HOME` and it should print the path you provided earlier.


Finally, Apache Airflow can be installed with `pip3 install apache-airflow`. **Remember to have virtual environment activated!**

Then, in accordance with default *airflow.cfg* configuration a new folder for your DAGs should be created inside $AIRFLOW_HOME. We can create a folder when we are in Linux terminal in proper directory with a command: `mkdir dags`


### Airflow Initialization and User Creation
Finally, we can initialise our scheduler and create a user
```sh
cd $AIRFLOW_HOME
airflow db init
airflow users create -u <username> -f <firstName> -l <lastName> -r Admin -e <emaill@adress>
```
And from the same terminal we can run `airflow scheduler` to start main component of Apache Airflow.

To access graphic UI we must open a new WSL terminal and repeat few steps:
```sh
source airflow_env/bin/activate
cd $AIRFLOW_HOME
airflow webserver
```
And now, you can access the graphical interface of Apache Airflow at *localhost:8080*. You’re ready to go!
