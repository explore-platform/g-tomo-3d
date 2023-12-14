# ACTUAL IMAGE
FROM ubuntu:20.04

WORKDIR /sda/

# ==============================================
# COMMON INSTALLS
# ==============================================
RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt update
RUN apt install -y python3.8 python3.8-venv  python-is-python3 python3-pip nginx curl wget \
    python3-distutils python3-apt python3-dev python3-wheel git

# TEMP
# ==============================================
# VISUALISER
# ==============================================
RUN apt-get install -y nodejs npm gnupg
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org


# Use NodeJS 16.x - Ubuntu default is 12.x
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs gnupg

# Install PhantomJS prebuilt - required when building visualizer (module dependency)
RUN npm install phantomjs-prebuilt -g


# Install ArangoDB for visualizer annotations
RUN echo 'deb https://download.arangodb.com/arangodb34/DEBIAN/ /' | tee /etc/apt/sources.list.d/arangodb.list
RUN wget -q https://download.arangodb.com/arangodb34/DEBIAN/Release.key -O- | apt-key add - 
RUN apt update
RUN apt -y install apt-transport-https
RUN echo arangodb3 arangodb3/password password root | debconf-set-selections
RUN echo arangodb3 arangodb3/password_again password root | debconf-set-selections
RUN echo arangodb3 arangodb3/upgrade boolean true | debconf-set-selections
RUN echo arangodb3 arangodb3/storage_engine	select auto | debconf-set-selections
RUN echo arangodb3 arangodb3/backup	boolean false | debconf-set-selections
RUN apt -y install arangodb3

RUN git config --global http.sslVerify false
RUN git clone -b visualizer_v3_explore_dev_guidanceUI https://gitlab-ci-token:glpat-r_RJRyskgStudyhrhaUB@gitlab.know-center.tugraz.at/visualizer/visualizer.git /visualizer

RUN chmod +x  /visualizer/startApplications.sh
# install node packages
WORKDIR /visualizer/
RUN npm install
#WORKDIR /sda/
#COPY visualiser/arangoDbConfig.js /visualizer/app/config/
WORKDIR /visualizer/
RUN npm run build

WORKDIR /sda/

# create virtual env and install python packages
#RUN python -m venv /venv/visualiser_env
#RUN /venv/visualiser_env/bin/pip install wheel
#RUN /venv/visualiser_env/bin/pip install memory-profiler
#RUN /venv/visualiser_env/bin/pip install -r /visualizer/app/wizard/requirements.txt #-> TODO us this hoever add memory profiler due to docker file
# ==============================================
# BIAS DETECTION
# ==============================================
#RUN git clone https://gitlab-ci-token:glpat-FU_Nz1DE-sAjhxm1ttqx@gitlab.know-center.tugraz.at/visualizer/bias-detection-fastapi.git /biasdetection

# create virtual env and install python packages
#RUN python -m venv /venv/biasdetection_env
#RUN /venv/biasdetection_env/bin/pip install -r /biasdetection/requirements.txt


# ==============================================
# PIP INSTALLS (fast docker build)
# ==============================================

# MACHINE LEARNING LIBS
RUN python -m venv /venv/machine_learning_env
COPY  ./machine_learning/requirements.txt  ./machine_learning/requirements.txt
RUN /venv/machine_learning_env/bin/pip install -r ./machine_learning/requirements.txt

# SCIENCE LIBS
RUN python -m venv /venv/science_env
RUN /venv/science_env/bin/pip install wheel 
RUN /venv/science_env/bin/pip install memory-profiler
COPY ./science/requirements.txt  ./science/requirements.txt
RUN /venv/science_env/bin/pip install -r ./science/requirements.txt

ENV dash_port=8050
ENV dash_debug="False"
EXPOSE 8050

# ==============================================
# COPY ALL FILES
# ==============================================
COPY . .

# ==============================================
# NGINX
# ==============================================
COPY ./_prod/nginx.conf /etc/nginx/nginx.conf
COPY ./_prod/default.conf /etc/nginx/conf.d/default.conf

# ==============================================
# BUILD SCRIPTS
# ==============================================
RUN bash machine_learning/build.sh
RUN bash science/build.sh
RUN bash visualiser/build.sh


# ==============================================
# ENTRYPOINTS
# ==============================================
ENTRYPOINT bash ./_prod/run.sh