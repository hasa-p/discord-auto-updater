# Discord Auto-Updater for Linux

A lightweight Python service that automatically keeps Discord up-to-date on Debian-based Linux distributions. Designed for users who prefer native `.deb` packages over Snap or Flatpak.

## Features

- **Automatic update checks** - Runs at system startup via systemd
- **Seamless installation** - Downloads and installs the latest `.deb` package
- **Desktop notifications** - Distro-agnostic notifications keep you informed
- **Auto-launch** - Starts Discord automatically after updating
- **Native package management** - Works with `.deb` packages, no Snap/Flatpak required

## Requirements

- Debian-based Linux distribution (Ubuntu, Linux Mint, Debian, etc.)
- Python 3.6+
- `sudo` privileges (for installing `.deb` packages)
