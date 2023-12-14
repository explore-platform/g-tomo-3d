FROM ubuntu:20.04

WORKDIR /sda/

# ==============================================
# COMON INSTALLS
# ==============================================
RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt update
RUN apt install -y python3.8 python3.8-venv python-is-python3 python3-pip curl nginx
RUN python --version
RUN python -m pip --version

# ==============================================
# PIP INSTALLS (fast docker build)
# ==============================================

# MACHINE LEARNING LIBS
RUN python -m venv /venv/machine_learning_env
COPY  ./machine_learning/requirements.txt  ./machine_learning/requirements.txt
RUN /venv/machine_learning_env/bin/pip install -r ./machine_learning/requirements.txt

# SCIENCE LIBS
RUN python -m venv /venv/science_env
COPY  ./science/requirements.txt  ./science/requirements.txt
RUN /venv/science_env/bin/pip install -r ./science/requirements.txt

# ==============================================
# COPY ALL FILES
# ==============================================
COPY . .

# ==============================================
# NGINX
# ==============================================
COPY ./_local/nginx.conf /etc/nginx/nginx.conf
COPY ./_local/default.conf /etc/nginx/conf.d/default.conf

# ==============================================
# BUILD SCRIPTS
# ==============================================
RUN bash machine_learning/build.sh
RUN bash science/build.sh
RUN bash visualiser/build.sh

# ==============================================
# ENTRYPOINTS
# ==============================================
ENTRYPOINT bash ./_local/run.sh