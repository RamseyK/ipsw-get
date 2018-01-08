# ipsw-get - A tool to automate the bulk download of IPSWs
https://github.com/RamseyK/ipsw-get


Python script to automate the bulk download of IPSWs with a specific criteria. Powered by http://ipsw.me

## Usage:

```bash
// "Download all iPod firmwares iOS 10 and above"
ipsw-get.py -device ipod -min 10 -o /Volumes/MEDIA/ipsws

// Download all iPhone firmwares between iOS 8.4 and 9.3.5
ipsw-get.py -device iphone -min 8.4 -max 9.3.5 -o /Volumes/MEDIA/ipsws

// Download all AppleTV5,3 (Apple TV 4 - 2015) firmwares between 11.0 and 11.1.2
ipsw-get.py -device appletv5,3 -min 11 -max 11.1.2 -o /Volumes/MEDIA/ipsws

// Download all iPadPro firmwares
ipsw-get.py -device ipadpro -o /Volumes/MEDIA/ipsws

// Download all iOS firmwares 11 and above
ipsw-get.py -min 11 -o /Volumes/MEDIA/ipsws

```


```bash
usage: ipsw-get.py [-h] [-min MIN_VERSION] [-max MAX_VERSION]
                     [-device DEVICE_IDENTIFIER] -o OUTPUT

A tool to automate the bulk download of IPSWs using ipsw.me

optional arguments:
  -h, --help            show this help message and exit
  -min MIN_VERSION, --min-version MIN_VERSION
                        Minimum iOS version
  -max MAX_VERSION, --max-version MAX_VERSION
                        Maximum iOS version
  -device DEVICE_IDENTIFIER, --device-identifier DEVICE_IDENTIFIER
                        Full or partial device identifier to filter on (eg.
                        iPhone7,2 / iPhone / iPod)
  -o OUTPUT, --output OUTPUT
                        Output directory to download files to
```
