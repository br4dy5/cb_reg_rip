# cb_reg_rip
This script will retrieve all SSIDs and corresponding first and last connection times from the registry of a remote host using Carbon Black Go Live. 

## Install Dependencies
It's expected that you're an authorized user of Carbon Black Response, but if you have not yet configured your API, instructions can be found here: https://cbapi.readthedocs.io/en/latest/#api-credentials
    
    pip install -r requirements.txt
    
## Usage
usage: cb_reg_rip.py [-h] hostname

positional arguments:

hostname        hostname of machine

optional arguments:

-h, --help  show this help message and exit

### Example
    cb_reg_rip.py hostname123
    
### Example Output
    Host is Online
    Current Time:  2018-01-24 15:32:43
    Next Check-In: 0:00:04

    Host is now available: https://123.45.6.789:1234/#/host/123456

    Google Starbucks
    first connected: 2018-01-20 10:03:31
    last connected: 2018-01-24 16:26:33
    
    FIOS-XYZ
    first connected: 2017-09-15 02:45:31
    last connected: 2017-09-16 23:26:33
    
