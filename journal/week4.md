# Week 4 — Postgres and RDS

## TL;DR

## Provision RDS Instance

You can both provision via the web console and via the CLI (there are also other options):

```sh
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username root \
  --master-user-password $RDS_PASSWORD \
  --allocated-storage 20 \
  --availability-zone eu-west-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

> This will take about 10-15 mins

> I've chosen to keep `performance insights` enabled because it's free if you've 7 days of retention period.

We can temporarily stop the RDS instance for __7 days__ when we aren't using it, __after that time the instance will automatically start again__.

Useful command for listing availability zones within a region:
```sh
aws ec2 describe-availability-zones --region eu-central-1
```

![Week 4 RDS CLI proof](assets/week4-rds-cli-console-proof.png)

## Connect via psql client

To connect to psql via the psql client cli tool remember to use the host flag to specific localhost and start your local pg container with `docker compose up db`.

```
psql -Upostgres --host localhost
```

Common PSQL commands:

```sql
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```

## Create (and dropping) our database

We can use the createdb command to create our database:

https://www.postgresql.org/docs/current/app-createdb.html

```
createdb cruddur -h localhost -U postgres
```

```sh
psql -U postgres -h localhost
```

```sql
\l
DROP database cruddur;
```

We can create the database within the PSQL client

```sql
CREATE database cruddur;
```
![Week4 create db cruddur psql proof](assets/week4-create-db-cruddur-psql-proof.png)

## Import Script

We'll create a new SQL file called `schema.sql`
and we'll place it in `backend-flask/db`

The command to import:
```
psql.exe -h localhost -U postgres cruddur < db/schema.sql
```

NOTE: We're creating it manually because Flask doesn't have this feature OOTB like other frameworks.

## Add UUID Extension

We are going to have Postgres generate out UUIDs (Universal Unique IDentifiers).
These are useful for obscuring info like the number of users registered on our service.
We'll need to use an extension called:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## Faster psql manual connection

Create and export an ENV_VAR like this one:

```sh
export CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
```

And use it without needing to write the password every time:

```sh
psql $CONNECTION_URL
```

We'll do the same for the production connection string.
> Remember to open the RDS SecurityGroup at least to your IP.

![Week4 psql cli connect proof](assets/week4-psql-cli-connect-proof.png)

## Shell Script to Connect to DB

For things we commonly need to do we can create a new directory called `bin`

We'll create an new folder called `bin` to hold all our bash scripts.

```sh
mkdir /workspace/aws-bootcamp-cruddur-2023/backend-flask/bin
```

```sh
export CONNECTION_URL="postgresql://postgres:pssword@127.0.0.1:5433/cruddur"
gp env CONNECTION_URL="postgresql://postgres:pssword@127.0.0.1:5433/cruddur"
```

We'll create a new bash script `bin/db-connect`

```sh
#! /usr/bin/bash

psql $CONNECTION_URL
```

We'll make it executable:

```sh
chmod u+x bin/db-connect
```

To execute the script:
```sh
./bin/db-connect
```

## Shell script to drop the database

`bin/db-drop`

```sh
#! /usr/bin/bash

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "DROP database cruddur;"
```

https://askubuntu.com/questions/595269/use-sed-on-a-string-variable-rather-than-a-file

## Test remote access

We'll create a connection url:

```
postgresql://root:huEE33z2Qvl383@cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com:5433/cruddur
```

We'll test that it works in Gitpod:

```sh
psql postgresql://root:huEE33z2Qvl383@cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com:5432/cruddur
```

We'll update your URL for production use case

```sh
export PROD_CONNECTION_URL="postgresql://root:huEE33z2Qvl383@cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com:5432/cruddur"
gp env PROD_CONNECTION_URL="postgresql://root:huEE33z2Qvl383@cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com:5432/cruddur"
```

## Update Bash scripts for production

```sh
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
else
  echo "Running in development mode"
fi
```

We then update:
- db-connect
- db-schema-load

## Shell script to create the database

`bin/db-create`

```sh
#! /usr/bin/bash

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
createdb cruddur $NO_DB_CONNECTION_URL
```

## Shell script to load the schema

`bin/db-schema-load`

```sh
#! /usr/bin/bash

schema_path="$(realpath .)/db/schema.sql"

echo $schema_path

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL cruddur < $schema_path
```

https://youtu.be/EtD7Kv5YCUs 1:39:34

## Shell script to load the seed data

```
#! /usr/bin/bash

#echo "== db-schema-load"


schema_path="$(realpath .)/db/schema.sql"

echo $schema_path

psql $CONNECTION_URL cruddur < $schema_path
```

## Make prints nicer

We we can make prints for our shell scripts coloured so we can see what we're doing:

https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux


```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
```

## Create our tables

https://www.postgresql.org/docs/current/sql-createtable.html

NOTE: Remember to `DROP` the tables before:

```sql
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
```

```sql
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text NOT NULL,
  handle text NOT NULL,
  email text NOT NULL,
  cognito_user_id text NOT NULL,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

```sql
CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

![Week4 seeds proof](assets/week4-seeds-proof.png)

> https://aviyadav231.medium.com/automatically-updating-a-timestamp-column-in-postgresql-using-triggers-98766e3b47a0

```sql
DROP FUNCTION IF EXISTS func_updated_at();
CREATE FUNCTION func_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

```sql
CREATE TRIGGER trig_users_updated_at 
BEFORE UPDATE ON users 
FOR EACH ROW EXECUTE PROCEDURE func_updated_at();
CREATE TRIGGER trig_activities_updated_at 
BEFORE UPDATE ON activities 
FOR EACH ROW EXECUTE PROCEDURE func_updated_at();
```

```sql
DROP TRIGGER IF EXISTS trig_users_updated_at ON users;
DROP TRIGGER IF EXISTS trig_activities_updated_at ON activities;
```

## See what connections we are using

Create `db-show-connections`:

```sh
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL --command="select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```

> We could have idle connections left open by our Database Explorer extension, try disconnecting and checking again the sessions 

## Easily setup (reset) everything for our database

```sh
#! /usr/bin/bash
-e # stop if it fails at any point

#echo "==== db-setup"

bin_path="$(realpath .)/bin"

source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```

## Install Postgres Client

https://www.psycopg.org/psycopg3/

We'll add the following to our `requirements.txt`

```
psycopg[binary]
psycopg[pool]
```

```
pip install -r requirements.txt
```

We need to set the env var for our backend-flask application:

```yml
  backend-flask:
    environment:
      CONNECTION_URL: "${CONNECTION_URL}"
```

## DB Object and Connection Pool

The purpose of connection pooling is to reuse a connection rather than dropping and recreating connections continuously.
That's better for both performance and to not hit the max number connection limit.

`lib/db.py`

```py
from psycopg_pool import ConnectionPool
import os

def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
  return sql

def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
  return sql

connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)
```

In our home activities we'll replace our mock endpoint with real api call:

```py
from lib.db import pool, query_wrap_array

      sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
      print(sql)
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
      return json[0]
```

![Week4 db pool fetch proof.png](assets/week4-db-pool-fetch-proof.png)

## Connect to RDS via Gitpod

> I didn't need this because I'm working from a local environment.

In order to connect to the RDS instance we need to provide our Gitpod IP and whitelist for inbound traffic on port 5432.

```sh
GITPOD_IP=$(curl ifconfig.me)
```

We'll create an inbound rule for Postgres (5432) and provide the GITPOD ID.

We'll get the security group rule id so we can easily modify it in the future from the terminal here in Gitpod.

```sh
export DB_SG_ID="sg-exampleeeeee"
gp env DB_SG_ID="sg-exampleeeeee"
export DB_SG_RULE_ID="sgr-testeateaet"
gp env DB_SG_RULE_ID="sgr-testeateaet"
```

Whenever we need to update our security groups we can do this for access.
```sh
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```

https://docs.aws.amazon.com/cli/latest/reference/ec2/modify-security-group-rules.html#examples

## Update Gitpod IP on new env var

We'll add a command step for postgres:

```sh
    command: |
      export GITPOD_IP=$(curl ifconfig.me)
      source "$THEIA_WORKSPACE_ROOT/backend-flask/db-update-sg-rule"
```

Testing the application connected to RDS without the schema loaded:

![Week4 RDS noseeds proof](assets/week4-rds-noseeds-proof.png)

Schema loaded to RDS db:

![Week4 RDS schema proof](assets/week4-rds-schema-proof.png)

## Setup Cognito post confirmation lambda

This Lambda will create a user record insed our DB after a user has been added/registered to the cognito pool.

### Create the handler function

- Create lambda in the same VPC as RDS instance in Python 3.8;
- Add a layer for psycopg2 with one of the below methods for development or production;
- Create the right roles and security groups for letting your lamba get to connect to the RDS instance.

ENV variables needed for the lambda environment:

```
CONNECTION_URL='postgresql://redacted'
```

The function:

```
import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)

    user_display_name  = user['name']
    user_email = user['email']
    user_handle = user['preferred_username']
    user_cognito_id = user['sub']
    try:
      print('entered-try')
      sql = f"""
         INSERT INTO public.users (
          display_name, 
          email,
          handle, 
          cognito_user_id
          ) 
        VALUES('{user_display_name}','{user_email}','{user_handle}','{user_cognito_id}')
      """
      print('SQL Statement: ')
      print(sql)
      conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
      cur = conn.cursor()
      cur.execute(sql)
      conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
          cur.close()
          conn.close()
          print('Database connection closed.')
    return event
```

![Week4 Lambda proof](assets/week4-lambda-proof.png)

### Development

This is where you can find the binary:

https://github.com/AbhimanyuHK/aws-psycopg2

`
This is a custom compiled psycopg2 C library for Python. Due to AWS Lambda missing the required PostgreSQL libraries in the AMI image, we needed to compile psycopg2 with the PostgreSQL libpq.so library statically linked libpq library instead of the default dynamic link.
`

`EASIEST METHOD`

Some precompiled versions of this layer are available publicly on AWS freely to add to your function by ARN reference.

https://github.com/jetbridge/psycopg2-lambda-layer

- Just go to Layers + in the function console and add a reference for your region. 

> NOTE: the region has to match the lambda one

`arn:aws:lambda:eu-central-1:898466741470:layer:psycopg2-py38:1`


Alternatively you can create your own development layer by downloading the psycopg2-binary source files from https://pypi.org/project/psycopg2-binary/#files

- Download the package for the lambda runtime environment: [psycopg2_binary-2.9.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl](https://files.pythonhosted.org/packages/36/af/a9f06e2469e943364b2383b45b3209b40350c105281948df62153394b4a9/psycopg2_binary-2.9.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl)

- Extract to a folder, then zip up that folder and upload as a new lambda layer to your AWS account

### Production

Follow the instructions on https://github.com/AbhimanyuHK/aws-psycopg2 to compile your own layer from postgres source libraries for the desired version.


## Add the function to Cognito 

Under the user pool properties add the function as a `Post Confirmation` lambda trigger.
You can find this option in the `User Pool Properties`.

![week4-lambda-cognito-signup-proof](assets/week4-lambda-cognito-signup-proof.png)

## Creating activities

We now want to add activities from our application and we want to store them in our database.

We'll work on the service `create-activity`.

Then we'll generally improve the application creating a better `Db` class that manages the interaction with the database in a central place.

For improving it we then create dedicated `.sql` files for separating the SQL code from the application code, they work like a sort of template.

What's shown in the video is working because the `user_handle` is hardcoded and matches the Andrew's handle.
One solution could be to harcode our `user_handle` too but a better solution would be to send the `Bearer Authorization` token to the endpoint, validate it and extract the `user_handle` info from that.
This solution is better because it's when we'll have more users we have to handle them correctly and more secure because we leverage the `JWT token`.
I couldn't find a way for fetching the `preferred_username` so I adapted the code for using the `cognito_user_id`.

The final result is that we can add activities: send them from the frontend, to and API endpoint via `POST`, save the record to the database
and then fetch it from the DB so it can be shown back by the frontend.

## Required Homeworks/Tasks
- Completed all the todo and technical tasks ✅
- Provision an RDS instance ✅
- Temporarily stop an RDS instance ✅
- Remotely connect to RDS instance ✅
- Programmatically update a security group rule ✅ (even if I'm working from a local environment)
- Write several bash scripts for database operations ✅
- Operate common SQL commands ✅
- Create a schema SQL file by hand ✅
- Work with UUIDs and PSQL extensions ✅
- Implement a postgres client for python using a connection pool ✅
- Troubleshoot common SQL errors ✅
- Implement a Lambda that runs in a VPC and commits code to RDS ✅
- Work with PSQL json functions to directly return json from the database ✅
- Correctly sanitize parameters passed to SQL to execute ✅
- Create new activities with a database insert ✅