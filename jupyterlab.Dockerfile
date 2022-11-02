FROM cluster-base

# -- Layer: JupyterLab

ARG spark_version=3.2.2
ARG jupyterlab_version=3.2.5

COPY ./ ${SHARED_WORKSPACE}/
# COPY ./redditStreaming/creds.json ${SHARED_WORKSPACE}
# COPY ./redditStreaming/fairscheduler.xml ${SHARED_WORKSPACE}
# COPY ./redditStreaming/requirements.txt ${SHARED_WORKSPACE}/redditStreaming/
# COPY ./redditStreaming/src/main/python/reddit/dist/reddit-0.1.0-py3-none-any.whl ${SHARED_WORKSPACE}/redditStreaming/src/main/python/reddit/dist/

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install pyspark==${spark_version} jupyterlab==${jupyterlab_version} && \
    python3 -m pip install /opt/workspace/src/main/python/twitter-main/dist/twitter-0.1.0-py3-none-any.whl && \
    python3 -m pip install -r /opt/workspace/src/main/python/env/requirements.txt --ignore-installed && \
    rm -rf /var/lib/apt/lists/*
    # ln -s /usr/local/bin/python3 /usr/bin/python

# deal w/ outdated pyspark guava jar for hadoop-aws (check maven repo for hadoop-common version)
RUN cd /usr/local/lib/python3.7/dist-packages/pyspark/jars/ && \
    mv guava-14.0.1.jar guava-14.0.1.jar.bk && \
    wget https://repo1.maven.org/maven2/com/google/guava/guava/27.0-jre/guava-27.0-jre.jar
# -- Runtime

EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}
CMD source twitter/bin/activate && python3 -m src/main/python/main.py

