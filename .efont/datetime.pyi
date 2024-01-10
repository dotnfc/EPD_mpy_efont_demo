"""
Module: 'datetime' 
"""

from typing import Any
from _typeshed import Incomplete

MINYEAR = 1 # type: int
MAXYEAR = 9999 # type: int

class timezone():
    def utcoffset(self, *args, **kwargs) -> Incomplete:
        ...

    def fromutc(self, *args, **kwargs) -> Incomplete:
        ...

    def dst(self, *args, **kwargs) -> Incomplete:
        ...

    def tzname(self, *args, **kwargs) -> Incomplete:
        ...

    def isoformat(self, *args, **kwargs) -> Incomplete:
        ...

    utc : Incomplete ## <class 'timezone'> = datetime.timezone(datetime.timedelta(microseconds=0), None)
    def __init__(self, *argv, **kwargs) -> None:
        ...


class timedelta():
    def total_seconds(self, *args, **kwargs) -> Incomplete:
        ...

    def isoformat(self, *args, **kwargs) -> Incomplete:
        ...

    def tuple(self, *args, **kwargs) -> Incomplete:
        ...

    microseconds : Incomplete ## <class 'property'> = <property>
    resolution : Incomplete ## <class 'timedelta'> = datetime.timedelta(microseconds=1)
    max : Incomplete ## <class 'timedelta'> = datetime.timedelta(microseconds=86399999999999999999)
    min : Incomplete ## <class 'timedelta'> = datetime.timedelta(microseconds=-86399999913600000000)
    seconds : Incomplete ## <class 'property'> = <property>
    days : Incomplete ## <class 'property'> = <property>
    def __init__(self, *argv, **kwargs) -> None:
        ...


class tzinfo():
    def utcoffset(self, *args, **kwargs) -> Incomplete:
        ...

    def dst(self, *args, **kwargs) -> Incomplete:
        ...

    def fromutc(self, *args, **kwargs) -> Incomplete:
        ...

    def tzname(self, *args, **kwargs) -> Incomplete:
        ...

    def isoformat(self, *args, **kwargs) -> Incomplete:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class datetime():
    def utcoffset(self, *args, **kwargs) -> Incomplete:
        ...

    def dst(self, *args, **kwargs) -> Incomplete:
        ...

    def toordinal(self, *args, **kwargs) -> Incomplete:
        ...

    def tzname(self, *args, **kwargs) -> Incomplete:
        ...

    def isoformat(self, *args, **kwargs) -> Incomplete:
        ...

    def timestamp(self, *args, **kwargs) -> Incomplete:
        ...

    def timetz(self, *args, **kwargs) -> Incomplete:
        ...

    def astimezone(self, *args, **kwargs) -> Incomplete:
        ...

    def timetuple(self, *args, **kwargs) -> Incomplete:
        ...

    def isoWeekNumber(self, *args, **kwargs) -> Incomplete:
        ...

    def isoweekday(self, *args, **kwargs) -> Incomplete:
        ...

    def time(self, *args, **kwargs) -> Incomplete:
        ...

    def weekday(self, *args, **kwargs) -> Incomplete:
        ...

    def date(self, *args, **kwargs) -> Incomplete:
        ...

    def tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def replace(self, *args, **kwargs) -> Incomplete:
        ...

    EPOCH : Incomplete ## <class 'datetime'> = datetime.datetime(2000, 1, 1, 0, 0, 0, 0, datetime.timezone(datetime.timedelta(microseconds=0), None), fold=0)
    hour : Incomplete ## <class 'property'> = <property>
    @classmethod
    def now(cls, *args, **kwargs) -> Incomplete:
        ...

    @classmethod
    def combine(cls, *args, **kwargs) -> Incomplete:
        ...

    minute : Incomplete ## <class 'property'> = <property>
    microsecond : Incomplete ## <class 'property'> = <property>
    second : Incomplete ## <class 'property'> = <property>
    year : Incomplete ## <class 'property'> = <property>
    day : Incomplete ## <class 'property'> = <property>
    fold : Incomplete ## <class 'property'> = <property>
    tzinfo : Incomplete ## <class 'property'> = <property>
    @classmethod
    def localtime(cls, *args, **kwargs) -> Incomplete:
        ...

    month : Incomplete ## <class 'property'> = <property>
    @classmethod
    def fromisoformat(cls, *args, **kwargs) -> Incomplete:
        ...

    @classmethod
    def fromordinal(cls, *args, **kwargs) -> Incomplete:
        ...

    @classmethod
    def fromtimestamp(cls, *args, **kwargs) -> Incomplete:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class date():
    def toordinal(self, *args, **kwargs) -> Incomplete:
        ...

    def isoformat(self, *args, **kwargs) -> Incomplete:
        ...

    def isoWeekNumber(self, *args, **kwargs) -> Incomplete:
        ...

    def timetuple(self, *args, **kwargs) -> Incomplete:
        ...

    def isoweekday(self, *args, **kwargs) -> Incomplete:
        ...

    def tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def weekday(self, *args, **kwargs) -> Incomplete:
        ...

    def replace(self, *args, **kwargs) -> Incomplete:
        ...

    max : Incomplete ## <class 'date'> = datetime.date(0, 0, 3652059)
    @classmethod
    def fromisoformat(cls, *args, **kwargs) -> Incomplete:
        ...

    day : Incomplete ## <class 'property'> = <property>
    year : Incomplete ## <class 'property'> = <property>
    month : Incomplete ## <class 'property'> = <property>
    min : Incomplete ## <class 'date'> = datetime.date(0, 0, 1)
    resolution : Incomplete ## <class 'timedelta'> = datetime.timedelta(microseconds=86400000000)
    @classmethod
    def fromordinal(cls, *args, **kwargs) -> Incomplete:
        ...

    @classmethod
    def fromtimestamp(cls, *args, **kwargs) -> Incomplete:
        ...

    @classmethod
    def today(cls, *args, **kwargs) -> Incomplete:
        ...

    def __init__(self, *argv, **kwargs) -> None:
        ...


class time():
    def utcoffset(self, *args, **kwargs) -> Incomplete:
        ...

    def isoformat(self, *args, **kwargs) -> Incomplete:
        ...

    def dst(self, *args, **kwargs) -> Incomplete:
        ...

    def tzname(self, *args, **kwargs) -> Incomplete:
        ...

    def tuple(self, *args, **kwargs) -> Incomplete:
        ...

    def replace(self, *args, **kwargs) -> Incomplete:
        ...

    minute : Incomplete ## <class 'property'> = <property>
    hour : Incomplete ## <class 'property'> = <property>
    second : Incomplete ## <class 'property'> = <property>
    @classmethod
    def fromisoformat(cls, *args, **kwargs) -> Incomplete:
        ...

    microsecond : Incomplete ## <class 'property'> = <property>
    min : Incomplete ## <class 'time'> = datetime.time(microsecond=0, tzinfo=None, fold=0)
    max : Incomplete ## <class 'time'> = datetime.time(microsecond=86399999999, tzinfo=None, fold=0)
    fold : Incomplete ## <class 'property'> = <property>
    resolution : Incomplete ## <class 'timedelta'> = datetime.timedelta(microseconds=1)
    tzinfo : Incomplete ## <class 'property'> = <property>
    def __init__(self, *argv, **kwargs) -> None:
        ...

