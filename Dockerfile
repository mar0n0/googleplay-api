ARG TAG=3.10

FROM python:${TAG}

ARG CONTAINER_USER="developer"
ARG LANGUAGE_CODE="en"
ARG COUNTRY_CODE="GB"
ARG ENCODING="UTF-8"

ARG LOCALE_STRING="${LANGUAGE_CODE}_${COUNTRY_CODE}"
ARG LOCALIZATION="${LOCALE_STRING}.${ENCODING}"

ARG OH_MY_ZSH_THEME="bira"

RUN apt update && apt -y upgrade && \
    apt -y install \
        locales \
        git \
        curl \
        sudo \
        nano \
        vim \
        inotify-tools \
        zsh && \
        echo "${LOCALIZATION} ${ENCODING}" > /etc/locale.gen && \
        locale-gen "${LOCALIZATION}" && \
        useradd -m -u 1000 -s /usr/bin/zsh "${CONTAINER_USER}" && \
        echo "${CONTAINER_USER}":"${CONTAINER_USER}" | chpasswd && adduser "${CONTAINER_USER}" sudo  && \
        bash -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" && \
        cp -v /root/.zshrc /home/"${CONTAINER_USER}"/.zshrc && \
        cp -rv /root/.oh-my-zsh /home/"${CONTAINER_USER}"/.oh-my-zsh && \
        sed -i "s/\/root/\/home\/${CONTAINER_USER}/g" /home/"${CONTAINER_USER}"/.zshrc && \
        sed -i s/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"${OH_MY_ZSH_THEME}\"/g /home/${CONTAINER_USER}/.zshrc && \
        mkdir /home/"${CONTAINER_USER}"/workspace && \
        chown -R "${CONTAINER_USER}":"${CONTAINER_USER}" /home/"${CONTAINER_USER}" && \
        mkdir /scripts_gpapi && \
        chown -R "${CONTAINER_USER}":"${CONTAINER_USER}" /scripts_gpapi

RUN apt install -y protobuf-compiler

ENV USER ${CONTAINER_USER}
ENV LANG "${LOCALIZATION}"
ENV LANGUAGE "${LOCALE_STRING}:${LANGUAGE_CODE}"
ENV PATH=/home/${CONTAINER_USER}/.local/bin:${PATH}
ENV LC_ALL "${LOCALIZATION}"
ENV PYTHONPATH=/home/${CONTAINER_USER}/python

WORKDIR /home/${CONTAINER_USER}/workspace

ADD . .

RUN chown -R "${CONTAINER_USER}":"${CONTAINER_USER}" /home/${CONTAINER_USER}/workspace

USER ${CONTAINER_USER}

RUN pip3 install 'protobuf<=3.20.1' --force-reinstall
RUN pip3 install -r /home/${CONTAINER_USER}/workspace/requirements.txt
RUN pip3 install -e .

RUN python setup.py build

CMD ["zsh"]

