#! python2


from cbapi.response import *
import datetime
import time
import argparse
import logging

# enable full logging for CB
# root = logging.getLogger()
# root.addHandler(logging.StreamHandler())
# logging.getLogger("cbapi").setLevel(logging.DEBUG)


usb_key1 = 'HKLM\System\ControlSet001\Control\DeviceClasses\{53f56307-b6bf-11d0-94f2-00a0c91efb8b}'
usb_key2 = 'HKLM\System\ControlSet001\Control\DeviceClasses\{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}'
net_key = 'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles'


def get_sensor():
    '''
    Returns the sensor ID of the hostname that is passed
    '''
    parser = argparse.ArgumentParser(description='Retrieves first and last connections to WiFi networks for provided hostname',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('hostname', help='hostname of machine')
    args = parser.parse_args()

    global hostname
    hostname = args.hostname

    cb = CbEnterpriseResponseAPI()
    global sensor
    sensor = cb.select(Sensor).where("hostname:" + hostname).first()


def get_status():
    '''
    Check to see if host is online
    '''
    tries = 0

    while sensor.status != "Online" and tries <= 12:
        now = datetime.datetime.now().replace(microsecond=0)
        last = sensor.last_checkin_time.replace(tzinfo=None, microsecond=0)
        since = now - last

        print "\nHost is Offline."
        print "Last Check-In Time: %s" % last
        print "Duration Since Last Check-In: %s" % since
        print "\nChecking again in 15 minutes"
        tries += 1
        time.sleep(900)

    if sensor.status == "Online":
        print "Host is Online"
        now = datetime.datetime.now().replace(microsecond=0)

        print "Current Time: ", now
        next_chk = sensor.next_checkin_time.replace(tzinfo=None, microsecond=0)
        next_left = next_chk - now

        # calculates remaining seconds til check-in, minus 2 to make sure it's listening before checked in
        next_secs = int(next_left.total_seconds()-2)
        if next_secs > 0:
            print "Next Check-In: %s" % next_left

            # prints status every 10 secs using count_down() function
            count_down(next_secs)

        print "\nHost is now available: " + sensor.webui_link + "\n"


def go_live():
    '''
    creates GoLive session, runs command
    '''

    global session
    with sensor.lr_session() as session:

        try:
            get_SSIDs()

        except:
            print "error running the GoLive command"


def get_SSIDs():
    '''
    Extract WiFi SSIDs and First & Last Connection Times
    '''

    key = session.list_registry_keys_and_values(net_key)
    for i in key['sub_keys']:
        value = session.list_registry_keys_and_values(
            'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\{0}'.format(i))
        ssid = value['values'][0]['value_data'][0]
        first_connect = value['values'][4]['value_data']
        last_connect = value['values'][6]['value_data']
        print ssid
        print "first connected: " + convert_date(first_connect)
        print "last connected: " + convert_date(last_connect)
        print "\n"


def count_down(sec_rem):
    '''
    prints time remaining every 10 seconds, on the tens place
    '''
    odd = sec_rem % 10
    time.sleep(odd)
    time_left = sec_rem - odd
    while time_left >= 10:
        print "{0} seconds remaining...".format(time_left)
        time.sleep(10)
        time_left -= 10


def convert_date(reg_date):
    '''
    pass the date value extracted from registry key
    returns date/time converted into human readable format: YYYY-M-D H:M:S 
    '''

    # convert extracted value from hex into ascii
    a = reg_date.decode("hex")

    # string locations for endian byte sequences reflecting date/time values
    yr = a[:4]
    mo = a[4:8]
    da = a[8:12]  # day of week, currently unused
    dy = a[12:16]
    hr = a[16:20]
    mn = a[20:24]
    sc = a[24:28]

    converted_date = convert(yr) + "-" + convert(mo) + "-" + convert(dy) + " " + convert(
        hr) + ":" + convert(mn) + ":" + convert(sc)
    return converted_date


def convert(endian):
    '''
    pass it a 4 char string in little endian
    returns in decimal
    '''

    first = endian[2:4]
    second = endian[0:2]
    swap = first + second

    conversion = str(int(swap, 16))

    # pad with leading 0 if only one digit
    if len(conversion) < 2:
        conversion = "0" + conversion
    # print conversion
    return conversion


def main():
    get_sensor()
    get_status()
    go_live()


if __name__ == "__main__":
    main()
