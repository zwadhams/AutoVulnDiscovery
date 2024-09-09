#!/bin/bash

# Download the image
curl -o /home/brittanyboles/AutoVulnDiscovery/Assignment1/CommandInjection/image.jpg "https://www.montana.edu/assets/images/1gq3l/image15.jpg"

sleep 3
# Set the background image

gsettings set org.gnome.desktop.background picture-uri 'file:////home/brittanyboles/AutoVulnDiscovery/Assignment1/CommandInjection/image.jpg'
