"""
Module: 'calender' 
"""
from typing import Any
from _typeshed import Incomplete

mdays = [] # type: list
NOVEMBER = 11 # type: int
DECEMBER = 12 # type: int
Month = [] # type: list
OCTOBER = 10 # type: int
JULY = 7 # type: int
AUGUST = 8 # type: int
SEPTEMBER = 9 # type: int
MONDAY = 0 # type: int
SATURDAY = 5 # type: int
SUNDAY = 6 # type: int
Day = [] # type: list
FRIDAY = 4 # type: int
TUESDAY = 1 # type: int
WEDNESDAY = 2 # type: int
THURSDAY = 3 # type: int
FEBRUARY = 2 # type: int
JUNE = 6 # type: int
JANUARY = 1 # type: int
MAY = 5 # type: int
MARCH = 3 # type: int
APRIL = 4 # type: int
def monthrange(*args, **kwargs) -> Incomplete:
    ...

def isleap(*args, **kwargs) -> Incomplete:
    ...

def leapdays(*args, **kwargs) -> Incomplete:
    ...

def weekday(*args, **kwargs) -> Incomplete:
    ...


class Calender():
    def monthdays2calendar(self, *args, **kwargs) -> Incomplete:
        ...

    def yeardayscalendar(self, *args, **kwargs) -> Incomplete:
        ...

    def monthdatescalendar(self, *args, **kwargs) -> Incomplete:
        ...

    def yeardays2calendar(self, *args, **kwargs) -> Incomplete:
        ...

    def monthdayscalendar(self, *args, **kwargs) -> Incomplete:
        ...

    def yeardatescalendar(self, *args, **kwargs) -> Incomplete:
        ...

    def getfirstweekday(self, *args, **kwargs) -> Incomplete:
        ...

    def setfirstweekday(self, *args, **kwargs) -> Incomplete:
        ...

    iterweekdays : Incomplete ## <class 'generator'> = <generator>
    firstweekday : Incomplete ## <class 'property'> = <property>
    itermonthdays3 : Incomplete ## <class 'generator'> = <generator>
    itermonthdates : Incomplete ## <class 'generator'> = <generator>
    itermonthdays : Incomplete ## <class 'generator'> = <generator>
    itermonthdays2 : Incomplete ## <class 'generator'> = <generator>
    itermonthdays4 : Incomplete ## <class 'generator'> = <generator>
    def __init__(self, *argv, **kwargs) -> None:
        ...


class IllegalWeekdayError(Exception):
    ...
