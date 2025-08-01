FROM apache/superset:latest

USER root

FROM apache/superset:latest

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      default-libmysqlclient-dev \
      pkg-config \
      python3-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      mysqlclient \
      pinotdb

COPY superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py

USER superset
ENTRYPOINT ["/superset-init.sh"]
