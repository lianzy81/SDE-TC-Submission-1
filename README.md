# Senior Data Enginer Tech Challenge: Submission
---
The submission is split into 5 sections:
1. Data Pipelines
2. Databases 
3. System Design
4. Charts & APIs
5. Machine Learning

---

## Section1: Data Pipelines
The data pipeline is implemented using airflow via docker containers with the following:
- Docker version 20.10.21
- docker-compose version 1.29.2
- Docker images
    - apache/airflow:2.4.3-python3.9
    - postgres:15.1

### (A) Run all of the containers used in the stack
    docker-compose up -d

### (B) Verify that the airflow-scheduler container is ready
    docker logs airflow-scheduler 

Once ready, you should see two log entries of "Booting worker with pid" and one log entry with "Launched DagFileProcessorManager"

### (C) Access the airflow stack
Once the airflow-scheduler is ready, the stack can be accessed on http://localhost:8080.
- Log in using the default username "airflow" and default password "airflow". 
- You should see one "data_pipeline_dag" in the DAGs page (see screenshot below).
- Refer to schedule, which is set as "15 * * * *", which means every hour at 15 minutes past the hour.
- Refer to next run for the datetime of the next scheduled run, which is set at 2022-12-22, 00:15.
- The "data_pipeline_dag" can be executed manually by pressing the "play" button under "Actions", followed by "Trigger DAG", which will generate the logs and outputs.
![airflow screenshot](./images/airflow_screenshot.png)

### (D) Input Raw Data
The input raw application data are located within the "data/raw" folder.

### (E) Scripts
The relevant Python scripts for the data pipeline are located at:
- airflow/dags/data_pipeline.py
- airflow/plugins/dataproc_config.py
- airflow/plugins/preprocess.py

### (F) Outputs
The processed data for successful and failed applications from each application dataset have been uploaded here and are located in the folders:
- "outputs/successful"
- "outputs/failed"

### (G) Logs
The data pipeline logs are stored under "airflow/logs/dag_id=data_pipeline_dag" with a separate log folder for each task as follows:
- task_id=task_id=ingest_and_process
- task_id=validity_check
Sample logs have been uploaed here under the same folder structure.

### (H) Tear down the airflow stack gracefully
    docker-compose down -v