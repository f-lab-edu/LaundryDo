FROM python:3.11

COPY requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1 # Not leaving any pycache
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR laundrydo

RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY . /${PROJECT_DIR}

WORKDIR /${PROJECT_DIR}

COPY run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
CMD ["./run.sh"]