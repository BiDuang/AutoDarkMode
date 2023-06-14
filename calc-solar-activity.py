# calculate and return sunrise, sunset time for given lat, long, and date using
# the method provided by NOAA Global Monitoring Division

from math import pi as PI
from math import cos as cos
from math import sin as sin
from math import tan as tan
from math import acos as arccos
import datetime as d
import pytz


def calc_sunrise_sunset(now: d.datetime, lat: float, long: float) -> tuple[d.datetime, d.datetime]:
    day_of_year = d.date.toordinal(now) - d.date.toordinal(d.datetime(now.year, 1, 1)) + 1
    year_length = 366 if is_leap_year(now.year) else 365
    hour = now.hour
    minute = now.minute
    second = now.second
    tz_offset = int(now.utcoffset().seconds / 3600) if (now.utcoffset().days != -1) else int((now.utcoffset().seconds - 86400) / 3600)
    lat_rad = lat * PI / 180
    # long_rad = long * PI / 180

    # calculate the fractional year (gamma), in radians
    gamma = 2 * PI / year_length * (day_of_year - 1 + (hour) / 24)

    # estimate the equation of time (in minutes) and the solar declination angle (in radians)
    eqtime = 229.18 * (0.000075 + 0.001868 * cos(gamma) - 0.032077 * sin(gamma) -
                       0.014615 * cos(2 * gamma) - 0.040849 * sin(2 * gamma))
    decl = (0.006918 - 0.399912 * cos(gamma) + 0.070257 * sin(gamma) - 0.006758 * cos(2 * gamma) +
            0.000907 * sin(2 * gamma) - 0.002697 * cos(3 * gamma) + 0.00148 * sin (3 * gamma))
    
    # find time offset (in minutes) and true solar time (in minutes)
    time_offset = eqtime + 4 * long - 60 * tz_offset
    tst = hour * 60 + minute + second / 60 + time_offset

    # solar hour angle (in radians)
    ha = ((tst / 4) - 180) * PI / 180

    # find solar zenith angle (phi) from the hour angle (ha), latitute (lat) and solar declination (decl)
    # cos_phi = sin(lat_rad) * sin(decl) + cos(lat_rad) * cos(decl) * cos(ha)
    # sin_phi = (1 - cos_phi ** 2) ** 0.5

    # find solar azimuth (theta, degrees clockwise from north)
    # cos_one_eighty_minus_theta = - (sin(lat) * cos_phi - sin(decl)) / cos(lat) * sin_phi

    # find the hour angles for sunrise/sunset, in degrees (zenith 90.833 degrees)
    ha_rise = (arccos(cos(1.5853349194640092) / cos(lat_rad) * cos(decl) - tan(lat_rad) * tan(decl))) / PI * 180
    ha_set = (-1) * ha_rise

    # find the UTC time of sunrise and sunset (in minutes)
    sunrise = 720 - 4 * (long + ha_rise) - eqtime
    sunset = 720 - 4 * (long + ha_set) - eqtime
    # solar_noon = 720 - 4 * long - eqtime

    sunrise_dt = d.datetime(now.year, now.month, now.day) + d.timedelta(hours=tz_offset, minutes=sunrise)
    sunset_dt = d.datetime(now.year, now.month, now.day) + d.timedelta(hours=tz_offset, minutes=sunset)
    return sunrise_dt, sunset_dt


def is_leap_year(year: int) -> bool:
    flag = False
    if year % 100 == 0:
        if year % 400 == 0:
            flag = True
    else:
        if year % 4 == 0:
            flag = True
    
    return flag


if __name__ == '__main__':
    now_naive = d.datetime.now()
    tz = pytz.timezone('Asia/Shanghai')
    now_aware = tz.localize(now_naive)

    sunrise, sunset = calc_sunrise_sunset(now_aware, 34.2658, 108.9541) # lat, long of Xi'an
    print(f"Sunrise and sunset time of today in Xi'an is {sunrise}, {sunset}") # 05:31, 19:58

# TODO: support half-hour timezones (for example India)
# TODO: support daylight saving time
