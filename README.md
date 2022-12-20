# Senior Data Enginer Tech Challenge: Submission
---
The submission is split into 5 sections:
1. Data Pipelines
2. Databases 
3. System Design
4. Charts & APIs
5. Machine Learning

All codes are implemented on an Ubuntu 20.04.5 LTS laptop with the following installed:
- Docker version 20.10.21
- docker-compose version 1.29.2
---

## Section 1: Data Pipelines
The required data pipeline is implemented using airflow via docker containers using the following Docker images:
- apache/airflow:2.4.3-python3.9
- postgres:15.1

### Scripts
The relevant Python scripts for the data pipeline are located at:
- airflow/dags/data_pipeline.py
- airflow/plugins/dataproc_config.py
- airflow/plugins/preprocess.py

### Execution Steps
#### (A) Start and run all of the containers used in the stack
    docker-compose up -d

#### (B) Verify that the airflow-scheduler container is ready
    docker logs airflow-scheduler 

Once ready, you should see two log entries of "Booting worker with pid" and one log entry with "Launched DagFileProcessorManager"

#### (C) Access the airflow stack
Once the airflow-scheduler is ready, the stack can be accessed on http://localhost:8080.
- Log in using the default username "airflow" and default password "airflow". 
- You should see one "data_pipeline_dag" in the DAGs page (see screenshot below).
- Refer to schedule, which is set as "15 * * * *", which means every hour at 15 minutes past the hour.
- Refer to next run for the datetime of the next scheduled run, which is set at 2022-12-22, 00:15.
- The "data_pipeline_dag" can be executed manually by pressing the "play" button under "Actions", followed by "Trigger DAG", which will generate the logs and outputs.
![airflow screenshot](./images/airflow_screenshot.png)

#### (D) Input Raw Data
The input raw application data are located within the "data/raw" folder.

#### (E) Outputs
The processed data for successful and failed applications from each application dataset have been uploaded here and are located in the folders:
- "outputs/successful"
- "outputs/failed"

#### (F) Logs
The data pipeline logs are stored under "airflow/logs/dag_id=data_pipeline_dag" with a separate log folder for each task as follows:
- task_id=task_id=ingest_and_process
- task_id=validity_check
Sample logs have been uploaed here under the same folder structure.

#### (G) Tear down the airflow stack gracefully
    docker-compose down -v


## Section 2: Databases

### Part 1: Setup sales transactions database for an e-commerce company
The required database for sales transactions is implemented via a postgres:15.1 Docker container. Additions have been made to the docker-compose.yml file used in Section 1 to start up the database service (container name db1) with the setup.sql file mounted inside the /docker-entrypoint-initdb.d directory within the container. This setup.sql file contains all relevant DDL statements needed to create an admin user ("dbadmin"), the sales database and associated tables. See ERD below for the tables created and their relationships. 

### Entity Relationship Diagram (ERD)

![ERD](./images/ERD_v1.png)

### SQL Scripts
You can find the setup.sql file with the DDL statements at the location "database/setup.sql".

### Execution Steps
#### (A) Start and run all of the containers used in the stack
    docker-compose up -d

#### (B) View the logs associated with the database and table creation inside the Docker container db1
    docker logs db1

#### (C) Enter into container db1, and then into postgres to view the tables created.
    docker exec -it db1 /bin/bash

#### (D) Connect to the sales database using the "dbadmin" user
    psql -d sales -U dbadmin

#### (E) List tables created in the sales database
    \dt

#### (F) View each table using SQL.
    select * from <table_name>;


### Part 2: Write SQL Statements for the following questions.

### Q1. Which are the top 10 members by spending?
```
    SELECT transactions.member_id, members.first_name, members.last_name, sum(transactions.total_items_price) as total_spending
    FROM transactions
    INNER JOIN members
    ON transactions.member_id = members.member_id
    GROUP BY (transactions.member_id, members.first_name, members.last_name)
    ORDER BY total_spending DESC
    LIMIT 10;
```

### Q2. Which are the top 3 items that are frequently brought by members?
```
    SELECT txn_details.item_id, items.item_name, sum(txn_details.quantity) as total_quantity
    FROM txn_details
    INNER JOIN items
    ON txn_details.item_id = items.item_id
    GROUP BY (txn_details.item_id, items.item_name)
    ORDER BY total_quantity DESC
    LIMIT 3;
```

The above SQL commands have also been added to the end of the setup.sql file. The outputs from the above queries can be viewed inside the logs for the database container. 

    docker logs db1


## Section 3: System Design

### Design 1
A role based access strategy will be suitable to meet the needs of the following teams:
- Logistics: 
    - Get the sales details (in particular the weight of the total items bought)
    - Update the table for completed transactions
- Analytics:
    - Perform analysis on the sales and membership status
    - Should not be able to perform updates on any tables
- Sales:
    - Update database with new items
    - Remove old items from database

The database/setup.sql file in Section 2 has been updated to implement the role based access strategy, One group role is created for each team above. Each group role is granted relevant permissions on specific tables to meet their needs as described below. 
-   logistics_user
    -   SELECT on items, txn_details, transactions
    -   INSERT, UPDATE on transactions
-   analytics_user
    -   SELECT on members, items, transactions, txn_details
-   sales_user
    -   SELECT, INSERT, UPDATE, DELETE on items

Thereafter, users can be created for specific members of each team, then assigned to their respective group roles to obtain the relevant permissions (see example SQL code below).

```
    CREATE USER log_user1 WITH ENCRYPTED PASSWORD 'log_user1';
    CREATE USER ana_user1 WITH ENCRYPTED PASSWORD 'ana_user1';
    CREATE USER sal_user1 WITH ENCRYPTED PASSWORD 'sal_user1';
    GRANT logistics_user to log_user1;
    GRANT analytics_user to ana_user1;
    GRANT sales_user to sal_user1;
```

### Design 2