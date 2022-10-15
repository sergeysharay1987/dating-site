Развертывание локальной среды разработки
========================================

Первоначальная установка
++++++++++++++++++++++++

#. Установить Docker по инструкции: https://docs.docker.com/engine/install/ubuntu/

#. Добавить своего пользователья в группу docker::

    sudo usermod -aG docker $USER
    exit

#. Установить ``pyenv`` по инструкции: https://github.com/pyenv/pyenv-installer
#. Установить необходимую версию Python::

    pyenv install 3.9.2

#. Установить Poetry::

    export PIP_REQUIRED_VERSION=22.2.2
    pip install pip==${PIP_REQUIRED_VERSION} && \
    pip install virtualenvwrapper && \
    pip install poetry==1.2.1 && \
    poetry config virtualenvs.path ${HOME}/.virtualenvs && \
    poetry run pip install pip==${PIP_REQUIRED_VERSION}


Запуск
++++++

#. (в отдельном окне терминала) Запустить сервисы с помощью Docker::

    make up-dependencies-only
