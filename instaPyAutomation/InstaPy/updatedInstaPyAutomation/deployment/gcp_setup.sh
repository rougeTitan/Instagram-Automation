#!/bin/bash
# Google Cloud Platform VM Setup Script for Instagram Automation
# Run this script after SSH into your GCP VM

set -e  # Exit on any error

echo "========================================================================"
echo "Instagram Bot - GCP Ubuntu Setup"
echo "========================================================================"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
echo "🐍 Installing Python 3.11..."
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set Python 3.11 as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install Chrome dependencies
echo "🌐 Installing Chrome and dependencies..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install -y google-chrome-stable

# Install ChromeDriver
echo "🚗 Installing ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} -O /tmp/chrome_version
CHROMEDRIVER_VERSION=$(cat /tmp/chrome_version)
wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O /tmp/chromedriver.zip
sudo apt install -y unzip
unzip /tmp/chromedriver.zip -d /tmp/
sudo mv /tmp/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm /tmp/chromedriver.zip /tmp/chrome_version

# Install Xvfb (Virtual Display for headless Chrome)
echo "🖥️  Installing Xvfb for headless mode..."
sudo apt install -y xvfb x11vnc x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps

# Install additional dependencies
echo "📚 Installing additional dependencies..."
sudo apt install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1

# Install Git
echo "📥 Installing Git..."
sudo apt install -y git

# Create project directory
echo "📁 Creating project directory..."
mkdir -p ~/instagram-bot
cd ~/instagram-bot

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python packages
echo "📦 Installing Python packages..."
pip install selenium undetected-chromedriver colorama python-dotenv google-generativeai pillow requests

# Create logs directory
mkdir -p ~/instagram-bot/logs

# Create systemd service directory if needed
mkdir -p ~/.config/systemd/user/

echo ""
echo "========================================================================"
echo "✅ Setup Complete!"
echo "========================================================================"
echo ""
echo "System Information:"
python3 --version
google-chrome --version
chromedriver --version
echo ""
echo "Next steps:"
echo "1. Upload your Instagram bot files to ~/instagram-bot/"
echo "2. Create .env file with your credentials"
echo "3. Run the cron setup script"
echo ""
echo "To activate virtual environment: source ~/instagram-bot/venv/bin/activate"
echo ""
