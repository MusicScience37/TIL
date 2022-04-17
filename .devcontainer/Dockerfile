FROM musicscience37/sphinx-doxygen:clang13-v4.2

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-client=1:8.2p1-4ubuntu0.4 \
    gnupg2=2.2.19-3ubuntu2.1 \
    vim=2:8.1.2269-1ubuntu5.7 \
    nano=4.8-1ubuntu1 && \
    apt-get autoremove && \
    apt-get autoclean
