# calculate and return sunrise, sunset time for given lat, long, and date using
# the method provided by NOAA Global Monitoring Division

from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz


def calc_sunrise_sunset(
    city: str,
    region: str,
    timezone: datetime.timezone,
    date: datetime.date,
    lat: float,
    long: float,
) -> tuple[datetime.datetime, datetime.datetime]:
    location = LocationInfo(city, region, timezone.__str__(), lat, long)
    s = sun(location.observer, date=date, tzinfo=timezone)
    return s["sunrise"], s["sunset"]


def is_leap_year(year: int) -> bool:
    flag = False
    if year % 100 == 0:
        if year % 400 == 0:
            flag = True
    else:
        if year % 4 == 0:
            flag = True

    return flag


if __name__ == "__main__":
    now_naive = datetime.datetime.now()
    tz = pytz.timezone("Asia/Shanghai")
    now_aware = tz.localize(now_naive)

    sunrise, sunset = calc_sunrise_sunset(
        "Xi'an", "China", tz, now_aware.date(), 34.2658, 108.9541
    )

    print(
        f"Sunrise and sunset time of today in Xi'an is {sunrise.strftime('%H:%M')}, {sunset.strftime('%H:%M')}"
    )  # 05:31, 19:58

# TODO: support half-hour timezones (for example India)
# TODO: support daylight saving time
