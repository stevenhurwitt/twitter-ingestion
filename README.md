# twitter-ingestion

Ingestion data from Twitter API using Spark, Kafka & Docker.

## 1. Install dependencies

### Python

`source twitter/bin/activate`
`cd src/main/python/env`

#### pip

`pip3 install -r requirements.txt`

#### conda

`conda create -n twitter -f twitter.yml`

### Scala

#### maven

`cd src/main/scala`
`mvn clean install && mvn clean package`

`which java && java src/main/scala/target/uber-twitter-*.jar`

#### sbt
`sbt build`
`sbt run`