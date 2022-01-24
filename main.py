#!/usr/bin/env python3

"""Simple python script to get useful times to take photos"""
import argparse
import enum
import dataclasses
import time

import numpy as np
import astropy.coordinates as coord
import astropy.time as at
import astropy.units as u
import termcolor

class Alt(enum.Enum):
    """Solar altitude ranges in degrees"""
    NIGHT: tuple = (-90 * u.deg, -18 * u.deg)
    TWILIGHT: tuple = (-18 * u.deg, -6 * u.deg)
    BLUE_HOUR: tuple = (-6 * u.deg, -4 * u.deg)
    GOLDEN_HOUR: tuple = (-4 * u.deg, 6 * u.deg)


@dataclasses.dataclass
class PhotoTimes():
    night: tuple = (None, None, None, None)
    twilight: tuple = (None, None, None, None)
    blue_hour: tuple = (None, None, None, None)
    golden_hour: tuple = (None, None, None, None)
    high_noon: tuple = (None, None)


def main() -> None:
    """Called only when run as script."""
    args = parse_args()

    if args.date == '':
        date = at.Time.now()
    else:
        date = at.Time(args.date)

    times, alts = get_sun_alts(
        args.location,
        args.interval,
        args.format,
        args.time_zone_shift_utc,
        date,
    )
    photo_times = get_photo_times(times, alts)
    print_photo_times(photo_times)


def parse_args() -> argparse.Namespace:
    """Returns arguments from command line"""
    parser = argparse.ArgumentParser()
    time_zone = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    time_zone /= -3600
    parser.add_argument(
        'location',
        help='any string that the Google Geocoding API can resolve'
    )
    
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=1,
        help='time precision interval in minutes. default = 1',
    )

    parser.add_argument(
        '-f', '--format',
        default='%H:%M',
        help='time format string. default = %%H:%%M',
    )

    parser.add_argument(
        '-z', '--time-zone-shift-utc',
        type=int,
        default=int(time_zone),
        help='hour shift from utc. default = system time zone',
    )

    parser.add_argument(
        '-d', '--date',
        default='',
        help='date to calculate for. format = YYYY-MM-DD. default = today',
    )
    return parser.parse_args()


def get_sun_alts(
    location: str,
    interval: int,
    time_format: str,
    time_zone_shift: int,
    date: at.Time,
) -> tuple[np.ndarray, np.ndarray]:
    """Returns the sun altitudes at a range of times"""
    today = int(date.to_value('mjd')) - time_zone_shift / 24
    loc = coord.EarthLocation.of_address(location)
    times = at.Time(np.arange(today, today + 1, interval / 60 / 24), format='mjd', location=loc)
    frames = coord.AltAz(obstime=times, location=loc)
    sun_alts = 90 * u.deg - coord.get_sun(times).transform_to(frames).zen
    times += time_zone_shift * u.hr
    return times.strftime(time_format), sun_alts


def get_photo_times(times: np.ndarray, sun_alts: np.ndarray) -> PhotoTimes:
    """Calculates photo times"""
    pt = PhotoTimes()
    iterator = zip(Alt, pt.__dataclass_fields__)
    max_idx = np.argmax(sun_alts)

    for bounds, bracket in iterator:
        lo, hi = bounds.value
        in_bracket = np.where((sun_alts > lo) & (sun_alts < hi))[0]
        if len(in_bracket) > 0:
            if in_bracket[0] > max_idx:
                start1 = end1 = None
                start2 = times[in_bracket[0]]
                end2 = times[in_bracket[-1]]
            else:
                bracket_diffs = np.diff(in_bracket)
                start1 = times[in_bracket[0]]

                if len(bracket_diffs) > 0 and np.amax(bracket_diffs) > 1:
                    in_bracket_idx = np.argmax(bracket_diffs)
                    end1 = times[in_bracket[in_bracket_idx]]
                    start2 = times[in_bracket[in_bracket_idx + 1]]
                    end2 = times[in_bracket[-1]]
                else:
                    end1 = times[in_bracket[-1]]
                    start2 = end2 = None

            setattr(pt, bracket, (start1, end1, start2, end2))

    if np.amax(sun_alts) > Alt.GOLDEN_HOUR.value[1]:
        pt.high_noon = (times[max_idx], sun_alts[max_idx])

    return pt


def print_photo_times(pt: PhotoTimes) -> None:
    """Prints the final result to the terminal"""
    iterator = [
        (pt.night[:2], 'night', 'white'),
        (pt.twilight[:2], 'twilight', 'magenta'),
        (pt.blue_hour[:2],'blue hour', 'blue'),
        (pt.golden_hour[:2], 'golden hour', 'red'),
        (pt.high_noon, 'high noon', 'yellow'),
        (pt.golden_hour[2:], 'golden hour', 'red'),
        (pt.blue_hour[2:],'blue hour', 'blue'),
        (pt.twilight[2:], 'twilight', 'magenta'),
        (pt.night[2:], 'night', 'white'),
    ]
    max_name_length = max([len(name) for _,name,_ in iterator])
    for field, name, color in iterator:
        if field[0] == None:
            continue
        if isinstance(field[1], coord.angles.Angle):
            ending = f', {field[1]:.2f}'
        else:
            ending = f' - {field[1]}'
        
        termcolor.cprint(
                f'{name:>{max_name_length}}: {field[0]}{ending}', color)


if __name__ == '__main__':
    main()
