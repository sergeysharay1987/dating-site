Развертывание локальной среды разработки
========================================

Первоначальная установка
++++++++++++++++++++++++

После первоначальной установки необходимо выполнять только раздел `Обновление`_ для обновления

#. Установить Docker по инструкции: https://docs.docker.com/engine/install/ubuntu/

#. Добавить своего пользователя в группу docker::

    sudo usermod -aG docker $USER
    exit

#. Установить зависимости (as prescribed at `<https://github.com/pyenv/pyenv/wiki/Common-build-problems>`_ ) ::

    apt update && \
    apt install make build-essential libssl-dev zlib1g-dev libbz2-dev \
                libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
                libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl \
                libpq-dev

#. Установить ``pyenv`` по инструкции: https://github.com/pyenv/pyenv-installer
#. Установить необходимую версию Python::

    pyenv install 3.9.2

#. Установить Poetry::

    export PIP_REQUIRED_VERSION=22.3
    pip install pip==${PIP_REQUIRED_VERSION} && \
    pip install setuptools==65.5.0 && \
    pip install virtualenvwrapper && \
    pip install poetry==1.2.1 && \
    poetry config virtualenvs.path ${HOME}/.virtualenvs && \
    poetry run pip install setuptools==65.5.0 && \
    poetry run pip install virtualenvwrapper && \
    poetry run pip install pip==${PIP_REQUIRED_VERSION}

Обновление
++++++++++

#. (в отдельном окне терминала) Запустить сервисы с помощью Docker::

    make up-dependencies-only

#. Запустить обновление::

    make update

Запуск
++++++

#. (в отдельном окне терминала) Запустить сервисы с помощью Docker::

    make up-dependencies-only

#. (в отдельном окне терминала) Запустить сервер::

    make run-server
