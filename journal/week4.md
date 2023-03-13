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

---- CHECKPOINT ---- 01:06:44

## Create our tables

