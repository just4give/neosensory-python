sudo apt-get update && \
sudo apt-get install -yq \
    build-essential \
    git wget  \
    bluetooth libbluetooth-dev libudev-dev libusb-1.0-0-dev \
    libusb-dev libdbus-1-dev libglib2.0-dev libical-dev libreadline-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-gi \
    python3-dbus \
    python3-setuptools \
  && sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*

  curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
  sudo apt-get install -y nodejs
  