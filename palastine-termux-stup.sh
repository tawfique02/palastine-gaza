
#!/bin/bash
#This script is written by tawfique Elahey.please, when you make this change, provide my name in hidden.
#May Allah bless us and protect our muslim ummah
# Colors for text
RESET="\e[0m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
BOLD="\e[1m"
RED="\e[31m"
BOX="\e[36m"  # Color for the box

# Function to display a message inside a box
display_in_box() {
    local message="$1"
    local len=${#message}
    local border=$(printf "%0.s=" $(seq 1 $((len + 4))))  # Create border of length len+4

    echo -e "${BOX}${border}${RESET}"
    echo -e "${BOX}  ${message}  ${RESET}"
    echo -e "${BOX}${border}${RESET}"
}

# Display script credit with box
clear
display_in_box "${BOLD}This script is developed for Muslim Ummah.[ALLAHU AKBER]${RESET}"

# Function to install required packages
install_packages() {
    echo -e "${YELLOW}${BOLD}   Installing All Required Packages! Please Wait...${RESET}"
    echo -e "${YELLOW}${BOLD}]────────────────────────────────────────────[${RESET}" | pv -qL 10
    packages=(
        "python"
        "cmatrix"
        "pv"
        "figlet"
        "ruby"
        "mpv"
        "python2"
        "termux-api"
        "python3"
        "tree"
        "nmap"
        "git"
        "curl"
        "wget"
        "php"
    )
    
    for pkg in "${packages[@]}"; do
        echo -e "Installing: ${GREEN}$pkg${RESET}"
        pkg install "$pkg" -y >/dev/null 2>&1
    done
    
    # Python packages via pip
    echo -e "Installing Python packages..."
    pip install lolcat random requests mechanize || echo -e "${RED}Failed to install Python packages!${RESET}"
    pip2 install bs4 requests || echo -e "${RED}Failed to install pip2 packages!${RESET}"
    
    echo -e "${CYAN}${BOLD}        INSTALLATION COMPLETED [✓]${RESET}" | pv -qL 12
    echo -e "${YELLOW}${BOLD}]────────────────────────────────────────────[${RESET}"
}

# Function to update system packages
update_system() {
    echo -e "${CYAN}${BOLD}Updating system packages...${RESET}"
    apt update && apt upgrade -y && apt autoremove -y
    echo -e "${CYAN}${BOLD}System update completed!${RESET}"
}

# Function to update Python packages
update_python_packages() {
    echo -e "${CYAN}${BOLD}Updating Python packages...${RESET}"
    pip install --upgrade lolcat random requests mechanize || echo -e "${RED}Failed to upgrade Python packages!${RESET}"
    pip2 install --upgrade bs4 requests || echo -e "${RED}Failed to upgrade pip2 packages!${RESET}"
    echo -e "${CYAN}${BOLD}Python packages update completed!${RESET}"
}

# Function to update individual package
update_individual_package() {
    read -p "Enter the name of the package you want to update: " package
    echo -e "${CYAN}${BOLD}Updating package: ${package}...${RESET}"
    pkg install "$package" -y >/dev/null 2>&1
    echo -e "${CYAN}${BOLD}Package update completed!${RESET}"
}

# Prompt user to choose an update option
update_menu() {
    echo -e "${CYAN}${BOLD}Select an update option:${RESET}"
    echo -e "${YELLOW}1) Update system packages${RESET}"
    echo -e "${YELLOW}2) Update Python packages${RESET}"
    echo -e "${YELLOW}3) Update individual package${RESET}"
    echo -e "${YELLOW}4) Exit update options${RESET}"
    read -p "Enter your choice: " choice
    
    case "$choice" in
        1)
            update_system
            ;;
        2)
            update_python_packages
            ;;
        3)
            update_individual_package
            ;;
        4)
            echo -e "${CYAN}${BOLD}Exiting update options.${RESET}"
            ;;
        *)
            echo -e "${RED}Invalid choice! Please select a valid option.${RESET}"
            update_menu
            ;;
    esac
}

# Prompt user to confirm running the installation
clear
echo -e "${CYAN}${BOLD}   Initializing Script... Please Wait...${RESET}"
termux-setup-storage

# Run the installation function
install_packages

# Ask if the user wants to update anything
echo -e "${CYAN}${BOLD}Would you like to update anything?${RESET}"
echo -e "${YELLOW}1) Yes${RESET}"
echo -e "${YELLOW}2) No${RESET}"
read -p "Enter your choice: " update_choice

if [[ "$update_choice" =~ ^[Yy]$ || "$update_choice" -eq 1 ]]; then
    update_menu
else
    echo -e "${CYAN}${BOLD}Skipping updates...${RESET}"
fi

# Script completed
echo -e "${CYAN}${BOLD}Installation and setup are complete!${RESET}"
display_in_box "${BOLD}This script is developed for Muslim Ummah.[ALLAHU AKBER]${RESET}"
