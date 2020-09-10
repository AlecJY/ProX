# ProX
Emulate an Xbox 360/One Controller as a Switch Pro Controller over Bluetooth

**This project is under development**

## Requirements
* Linux with controller drivers installed
* An Bluetooth adapter

## Installation
1. Make sure Xbox 360/One Controller driver is installed ([xpad](https://github.com/paroj/xpad) or [xow](https://github.com/medusalix/xow))
2. Follow the installation instructions in [joycontrol](https://github.com/mart1nro/joycontrol)
3. Run this command to install the dependencies
```
sudo pip3 install -r requirements.txt
```

## Usage
```
usage: prox.py [-h] [-d DEVICE_ID] [--spi_flash SPI_FLASH]
               [-r RECONNECT_BT_ADDR] [-x]

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE_ID, --device_id DEVICE_ID
  --spi_flash SPI_FLASH
  -r RECONNECT_BT_ADDR, --reconnect_bt_addr RECONNECT_BT_ADDR
                        The Switch console Bluetooth address, for reconnecting
                        as an already paired controller
  -x, --xbox_layout
```

## Known Issue
* Sometimes some buttons will be ignored when press multiple buttons at the same time

## TODO
* Vibration

## Credits
* [joycontrol](https://github.com/mart1nro/joycontrol)
* [xbox360controller](https://github.com/linusg/xbox360controller)