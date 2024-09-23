#!/bin/bash

# Download the image
curl -o "$(pwd)/image.jpg" "https://cdn.britannica.com/19/257919-050-20104F6A/still-from-free-solo-documentary-film-about-alex-honnold-climbing-el-capitan-wall-yosmite-2018.jpg"

# Set the downloaded image as the desktop background
gsettings set org.gnome.desktop.background picture-uri "file://$(pwd)/image.jpg"