#!/bin/bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Define the installation path
INSTALL_DIR="/home/pi/HoneyPet/honeypots/cowrie"

# Update the system
echo -e "${YELLOW}Updating the system...${NC}"
sudo apt update && sudo apt upgrade -y && echo -e "${GREEN}System updated successfully.${NC}" || echo -e "${RED}System update failed.${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
sudo apt install -y git python3 python3-pip build-essential libssl-dev libffi-dev libpython3-dev authbind && echo -e "${GREEN}Dependencies installed successfully.${NC}" || echo -e "${RED}Dependency installation failed.${NC}"

# Create the installation directory if it doesn't exist
echo -e "${YELLOW}Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Clone the Cowrie repository if it doesn't exist
if [ ! -d "$INSTALL_DIR/.git" ]; then
    echo -e "${YELLOW}Cloning the Cowrie repository...${NC}"
    git clone https://github.com/cowrie/cowrie.git . && echo -e "${GREEN}Cowrie repository cloned successfully.${NC}" || echo -e "${RED}Failed to clone Cowrie repository.${NC}"
else
    echo -e "${YELLOW}Cowrie repository already exists, skipping clone.${NC}"
fi

# Install Cowrie dependencies
echo -e "${YELLOW}Installing Cowrie dependencies...${NC}"
pip3 install --break-system-packages --upgrade pip && pip3 install --break-system-packages -r requirements.txt && echo -e "${GREEN}Cowrie dependencies installed successfully.${NC}" || echo -e "${RED}Failed to install Cowrie dependencies.${NC}"

# Upgrade cryptography and twisted to address deprecation warnings
echo -e "${YELLOW}Upgrading cryptography and twisted...${NC}"
pip3 install --break-system-packages --upgrade cryptography twisted && echo -e "${GREEN}Cryptography and twisted upgraded successfully.${NC}" || echo -e "${RED}Failed to upgrade cryptography and twisted.${NC}"

# Set up Cowrie configuration
echo -e "${YELLOW}Setting up Cowrie configuration...${NC}"
cp etc/cowrie.cfg.dist etc/cowrie.cfg && echo -e "${GREEN}Cowrie configuration set up successfully.${NC}" || echo -e "${RED}Failed to set up Cowrie configuration.${NC}"

# Create systemd service for Cowrie
SERVICE_FILE="/etc/systemd/system/cowrie.service"
if [ ! -f "$SERVICE_FILE" ]; then
    echo -e "${YELLOW}Creating Cowrie systemd service file...${NC}"
    sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Cowrie SSH and Telnet Honeypot
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash /home/pi/HoneyPet/honeypots/cowrie/bin/cowrie start
ExecStop=/bin/bash /home/pi/HoneyPet/honeypots/cowrie/bin/cowrie stop
Restart=always
User=pi
WorkingDirectory=/home/pi/HoneyPet/honeypots/cowrie

[Install]
WantedBy=multi-user.target
EOL
    echo -e "${GREEN}Cowrie systemd service file created successfully.${NC}"
else
    echo -e "${YELLOW}Cowrie systemd service file already exists.${NC}"
fi

# Reload systemd to recognize the new service
echo -e "${YELLOW}Reloading systemd daemon...${NC}"
sudo systemctl daemon-reload && echo -e "${GREEN}Systemd daemon reloaded successfully.${NC}" || echo -e "${RED}Failed to reload systemd daemon.${NC}"

# Enable and start the Cowrie service
echo -e "${YELLOW}Enabling and starting Cowrie service...${NC}"
sudo systemctl enable cowrie && sudo systemctl start cowrie && echo -e "${GREEN}Cowrie service enabled and started successfully.${NC}" || echo -e "${RED}Failed to enable or start Cowrie service.${NC}"

# Set ownership of the HoneyPet directory to the current user
echo -e "${YELLOW}Setting ownership of the HoneyPet directory...${NC}"
sudo chown -R pi:pi /home/pi/HoneyPet && echo -e "${GREEN}Ownership set successfully.${NC}" || echo -e "${RED}Failed to set ownership.${NC}"

# Print success message
echo -e "${GREEN}Cowrie has been installed and activated as a service successfully in $INSTALL_DIR.${NC}"
echo -e "${YELLOW}To start or stop the Cowrie service, use: sudo systemctl start cowrie or sudo systemctl stop cowrie.${NC}"
