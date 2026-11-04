# LxckyTools

A Python OSINT tool that allows you to turn Discord IDs into IP addresses using the Restorecord dataset. 

## Features

- **Discord Lookup**: Searches through 640k+ records in the Restorecord dataset to find a user's IP, username, and timestamp based on their Discord ID.
- **IP Lookup**: Built-in live IP lookup using a free, keyless API (`ipwhois`) to get location and ASN info.

## Setup

You just need Python and two libraries:

```bash
pip install rich ipwhois
```

Then run this when all the packages are installed 

```Powershell
python "C:\Users\User\Downloads\LxckyTools\lxckytools.py"
```

if it says missing dataset then run

```Powershell
cd "C:\Users\User\Downloads\LxckyTools" 
```

Then try

```Powershell
python lxckytools.py
```

# disclaimer 

the restorecord dataset is around a year old and this tool will not provide every discord users ip nor do we claim to
itll only retrive ip data of users that was in the restorecord dataset, also please make sure u use your file paths and not the examples above. 


