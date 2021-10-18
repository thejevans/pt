# pt
A simple script that shows important photography times. written in python.

```
usage: pt [-h] [-i INTERVAL] [-f FORMAT] [-z TIME_ZONE_SHIFT_UTC] [-d DATE] location

positional arguments:
  location              any string that the Google Geocoding API can resolve

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        time precision interval in minutes. default = 1
  -f FORMAT, --format FORMAT
                        time format string. default = %H:%M
  -z TIME_ZONE_SHIFT_UTC, --time-zone-shift-utc TIME_ZONE_SHIFT_UTC
                        hour shift from utc. default = system time zone
  -d DATE, --date DATE  date to calculate for. format = YYYY-MM-DD. default = today
```



requires:
`python >=3.8`
`numpy`
`astropy`
`termcolor`

![alt text](https://github.com/thejevans/pt/blob/main/screenshot.png)
