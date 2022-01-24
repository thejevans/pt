# pt

A simple script that shows important photography times. Written in python.

```bash
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
`python >=3.10`
`numpy`
`astropy`
`termcolor`

![alt text](https://github.com/thejevans/pt/blob/main/screenshot.png)

## Getting Started

To run from source, you will need:

1. Install Python version 3.10. [pyenv](https://github.com/pyenv/pyenv)
   recommended.
2. Install dependencies. [Virtualenv](https://virtualenv.pypa.io/en/latest/)
   recommended.

In depth:

```bash
pyenv install 3.10.1
pyenv local 3.10.1
virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Building

There's a `Makefile` which will use
[Pex](https://pex.readthedocs.io/en/v2.1.63/) to build a self-contained binary
that only depends on Python 3. Just run `make`, as long as you have `Virtualenv`
installed.
