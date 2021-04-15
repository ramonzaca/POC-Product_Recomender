# VERSION 0.1
# AUTHOR: Agustín Dye


FROM python:3.7
LABEL maintainer="Ramonzaca"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# If no enviroment is provided
ENV ENVIRONMENT=stage
# Change this ↑↑↑↑↑↑ to change enviroment

# For quicker building time
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY *   /

EXPOSE 5000

CMD ["python"  , "app.py"]

