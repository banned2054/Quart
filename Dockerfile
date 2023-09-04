# 使用 qbittorrent 的官方 Docker 镜像作为基础
FROM linuxserver/qbittorrent:latest

# 设置工作目录
WORKDIR /tmp

# 安装必要的依赖和工具
RUN apt-get update && \
    apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev

# 下载 Python 3.11 的源代码
RUN wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz && \
    tar -xvf Python-3.11.0.tgz

# 编译和安装 Python 3.11
WORKDIR /tmp/Python-3.11.0
RUN ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall

# 安装或升级 pip
RUN /usr/local/bin/python3.11 -m ensurepip && \
    /usr/local/bin/python3.11 -m pip install --upgrade pip

# 清理临时文件
WORKDIR /
RUN rm -rf /tmp/Python-3.11.0 && \
    rm /tmp/Python-3.11.0.tgz

# 设置默认的 Python 版本为 3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 1

# Set the working directory in the container to /app
WORKDIR /quart

# Add the current directory contents into the container at /app
ADD . /quart

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run run.sh when the container launches
CMD ["./run.sh"]