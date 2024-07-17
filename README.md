# PySpark Project Documentation

This document provides an overview and explanation of the PySpark project, focusing on the pipeline configuration files and acceptable attributes.

## Table of Contents

1. [Pipeline Configuration](#pipeline-configuration)
    - [Settings](#settings)
    - [Nodes](#nodes)
        - [Source Nodes](#source-nodes)
        - [Processor Nodes](#processor-nodes)
        - [Sink Nodes](#sink-nodes)
2. [Usage](#usage)

## Pipeline Configuration

The pipeline configuration file defines the settings and workflow for your PySpark project. It is written in YAML format and includes global Spark settings and node definitions. Below is an example of the configuration file and descriptions of acceptable attributes.

### Example Configuration File

```yaml
settings:
  "spark.app.name": "test-pipeline-ali"
  "spark.master": "spark://0.0.0.0:7077"
  "spark.driver.cores": "1"
  "spark.driver.memory": "1g"
  "spark.executor.instances": "2"
  "spark.cores.max": "4"
  "spark.executor.cores": "2"
  "spark.executor.memory": "2g"

nodes:
  test_mysql_db:
    type: "source"
    stream: false
    format: jdbc
    options:
      driver: "com.clickhouse.jdbc.ClickHouseDriver"
      url: "jdbc:clickhouse:http://0.0.0.0:8123/testDB"
      user: "default"
      password: ""
      database: "testDB"
      query: |
        select * from testDB.test

  test-process:
    type: "processor"
    format: query
    options:
      parents:
        - test_mysql_db
      query: |
       SELECT * FROM test_mysql_db

  sink_data:
    type: sink
    stream: false
    format: jdbc
    parent: "test-process"
    mode: append
    options:
      driver: "com.mysql.jdbc.Driver"
      url: "jdbc:mysql://0.0.0.0:3306/testDB"
      user: "test"
      password: "qwerty123456"
      database: "testDB"
      dbtable: test
```
Settings

The settings section contains global configurations for the Spark application. These settings are used to configure the SparkSession.

    "spark.app.name": Name of the Spark application.
    "spark.master": URL of the Spark master.
    "spark.driver.cores": Number of cores for the driver.
    "spark.driver.memory": Memory allocated for the driver.
    "spark.executor.instances": Number of executor instances.
    "spark.cores.max": Maximum number of cores for the application.
    "spark.executor.cores": Number of cores per executor.
    "spark.executor.memory": Memory allocated for each executor.

Nodes

The nodes section defines the data processing workflow. Each node can be a source, processor, or sink.
Source Nodes

Source nodes are used to read data from external sources.

    type: Must be "source".
    stream: Indicates if the source is a streaming source (true or false).
    format: Format of the source (e.g., jdbc).
    options: Configuration options specific to the source format.
        driver: JDBC driver class.
        url: JDBC URL.
        user: Username for the database.
        password: Password for the database.
        database: Name of the database.
        query: SQL query to fetch the data.

Processor Nodes

Processor nodes are used to transform data. Functions can be used to process and transform data in dataframes can be found in <a href="https://spark.apache.org/docs/latest/api/sql/">Spark SQL Built-in Functions</a>

    type: Must be "processor".
    format: Format of the processor (e.g., query).
    options: Configuration options for processing.
        parents: List of parent nodes (source nodes or other processing nodes).
        query: SQL query to transform the data.

Sink Nodes

Sink nodes are used to write data to external destinations.

    type: Must be "sink".
    stream: Indicates if the sink is a streaming sink (true or false).
    format: Format of the sink (e.g., jdbc).
    parent: Parent node (processor node).
    mode: Write mode (e.g., append).
    options: Configuration options specific to the sink format.
        driver: JDBC driver class.
        url: JDBC URL.
        user: Username for the database.
        password: Password for the database.
        database: Name of the database.
        dbtable: Name of the database table.

Usage

To use this configuration file, ensure that it is properly set up and saved in the specified path. The main.py script will parse this file and create a Spark DAG based on the nodes and settings defined.

## Source/Sink Node Types

The available source type in this PySpark project is the JDBC Connection Node, which provides connectivity to various databases such as MySQL, ClickHouse, PostgreSQL, etc. This node type allows you to specify JDBC parameters like driver, URL, username, password, database name, and query to fetch data. Additional Options available in <a href="https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html">Spark SQL JDBC</a>
