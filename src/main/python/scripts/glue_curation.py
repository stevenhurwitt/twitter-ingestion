from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
from delta import *
import datetime as dt
import pandas as pd
import numpy as np
import pprint
import boto3
import time
import json
import sys
import os

from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from delta.tables import *

pp = pprint.PrettyPrinter(indent = 1)
base = os.getcwd()


def main():
    ## init spark, sc
    args = getResolvedOptions(sys.argv, ["JOB_NAME"])
    host = "localhost"
    spark = sparkSession.builder.master("{}:7077".format(host)) \
            .config() \
            .config() \
            .config() \
            .enableHiveSupport() \
            .getOrCreate()

    sc = spark.SparkContext

    ## init glue job
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args["JOB_NAME"], args)

    subreddit = os.getenv(["twitter"])
    # subreddit = "technology"

    # init builder
    builder = SparkSession \
    .builder \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")

    # spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark = builder.getOrCreate()

    # read df as delta table from s3
    df = spark.read.format("delta").option("header", True).load("s3a://twitter-stevenhurwitt-final/" + subreddit)

    # transform df
    df = df.withColumn("approved_at_utc", col("approved_at_utc").cast("timestamp")) \
                    .withColumn("banned_at_utc", col("banned_at_utc").cast("timestamp")) \
                    .withColumn("created_utc", col("created_utc").cast("timestamp")) \
                    .withColumn("created", col("created").cast("timestamp")) \
                    .withColumn("year", year(col("date"))) \
                    .withColumn("month", month(col("date"))) \
                    .withColumn("day", dayofmonth(col("date"))) \
                    .withColumn("date", to_date(col("created_utc"), "MM-dd-yyyy")) \
                    .dropDuplicates(subset = ["title"])
                    
    # partition by year, month, day
    # write to delta on s3 (overwrite schema, headers)
    filepath = "s3a://twitter-stevenhurwitt/" + subreddit + "_clean/"
    df.write.format("delta") \
        .partitionBy("year", "month", "day") \
        .mode("overwrite") \
        .option("overwriteSchema", True) \
        .option("header", True) \
        .save(filepath)
            
    # vacuum delta table, general symlink manifest
    deltaTable = DeltaTable.forPath(spark, "s3a://twitter-stevenhurwitt-final/{}_clean".format(subreddit))
    deltaTable.vacuum(168)
    deltaTable.generate("symlink_format_manifest")

    # athena
    athena = boto3.client('athena')

    # repair table to use latest delta load
    athena.start_query_execution(
            QueryString = "MSCK REPAIR TABLE twitter.{}".format(subreddit),
            ResultConfiguration = {
                'OutputLocation': "s3://twitter-stevenhurwitt-final/_athena_results"
            })

    ## postgres mapping goes here...
    print("postgres coming soon...")

    # job.commit()
    sys.exit()

if __name__ == "__main__":
    main()
