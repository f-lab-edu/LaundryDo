FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1 # Not leaving any pycache
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR laundrydo

COPY requirements.txt /${PROJECT_DIR}/requirements.txt
WORKDIR /${PROJECT_DIR}/

RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY . /${PROJECT_DIR}/

RUN chmod +x /${PROJECT_DIR}/run.sh
# CMD ["sh", "run.sh"]