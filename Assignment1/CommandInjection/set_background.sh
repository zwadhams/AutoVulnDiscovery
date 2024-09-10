#!/bin/bash

# Download the image
curl -o "$(pwd)/image.jpg" "https://www.montana.edu/assets/images/1gq3l/image15.jpg"

# Set the downloaded image as the desktop background
gsettings set org.gnome.desktop.background picture-uri "file://$(pwd)/image.jpg"