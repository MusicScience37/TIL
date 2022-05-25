FROM musicscience37/sphinx-doxygen:clang14-v4.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-client \
    gnupg2 \
    vim \
    nano && \
    apt-get autoremove && \
    apt-get autoclean
