FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    x11-apps \
    x11-xserver-utils \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    dbus-x11 \
    git \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Generate locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Set the working directory to your project folder
WORKDIR /workspaces/recipe-book

# Create a virtual environment in a location outside the mounted workspace
RUN python3 -m venv --system-site-packages /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt /workspaces/recipe-book/requirements.txt
RUN pip install -r requirements.txt
