FROM ubuntu:18.04

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt-get -qq update && \
    apt-get -qq install --yes --no-install-recommends locales > /dev/null && \
    apt-get -y install wget git bzip2 curl python-pip cron && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*
ENV SHELL /bin/bash
RUN pip install awscli
RUN wget -q https://repo.continuum.io/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh -O /tmp/miniconda.sh  && \
    echo '718259965f234088d785cad1fbd7de03 */tmp/miniconda.sh' | md5sum -c - && \
    bash /tmp/miniconda.sh -f -b -p /opt/conda
RUN rm /tmp/miniconda.sh
COPY environment.yaml /tmp/environment.yaml
RUN /opt/conda/bin/conda env update -n base --file /tmp/environment.yaml
