from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from kafka import kafkaProducer, kafkaConsumer
from twitter_ingestion import *
from glue_curation import main
import datetime as dt
import json
import os

def main():
    print("starting...")
    twitter_ingestion()

if __name__ == "__main__":
    main()