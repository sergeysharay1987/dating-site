Local development environment
========================================

Initial setup
++++++++++++++++++++++++
Once initial setup is done only `Update`_  section should be performed to get the latest version for development.

#. Install Docker according to: https://docs.docker.com/engine/install/ubuntu/

#. Add your user to docker group::

    sudo usermod -aG docker $USER
    exit

#. Install dependencies (as prescribed at `<https://github.com/pyenv/pyenv/wiki/Common-build-problems>`_ ) ::

    apt update && \
    apt install make build-essential libssl-dev zlib1g-dev libbz2-dev \
                libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
                libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl \
                libpq-dev

#. Install ``pyenv`` according to: https://github.com/pyenv/pyenv-installer
#. Set a python version 3.9.2 in your directory with project::

    pyenv install 3.9.2

#. Install poetry, according to `<https://python-poetry.org/docs/#installation>`_::

    export PIP_REQUIRED_VERSION=22.3
    pip install pip==${PIP_REQUIRED_VERSION} && \
    pip install setuptools==65.5.0 && \
    pip install virtualenvwrapper && \
    pip install poetry==1.2.1 && \
    poetry config virtualenvs.path ${HOME}/.virtualenvs && \
    poetry run pip install setuptools==65.5.0 && \
    poetry run pip install virtualenvwrapper && \
    poetry run pip install pip==${PIP_REQUIRED_VERSION}

Update
++++++++++

#. (in a separate window of terminal) Run services using Docker::

    make up-dependencies-only

#. Run update::

    make update

Run
++++++

#. (in a separate window of terminal) Run services using Docker::

    make up-dependencies-only

#. (in a separate window of terminal) Run server::

    make run-server
