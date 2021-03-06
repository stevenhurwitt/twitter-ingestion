from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from kafka import kafkaProducer, kafkaConsumer
from twitter_ingestion import *
from glue_curation import main
import datetime as dt
import json
import os

with open("creds.json", "r") as f:
    creds = json.load(f)
    f.close()
    print("read creds.json")

def main():
    print("starting...")
    os.environ["AWS_ACCESS_KEY_ID"] = creds["aws-client"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = creds["aws-secret"]
    twitter_ingestion()

if __name__ == "__main__":
    main()