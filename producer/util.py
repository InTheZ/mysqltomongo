import random
import string
import time

from faker import Faker
import numpy as np

fake = Faker()

def randomMoney(min=0.00, max=100.00):
    return np.random.uniform(min, max)

def randomString(numDigits):
    return ''.join(random.choice(string.ascii_letters) for i in range(numDigits))

# use https://github.com/daviddrysdale/python-phonenumbers/tree/dev/python/phonenumbers
def randomPhoneNumber():
    areaCode =  ''.join(random.choice(string.digits) for i in range(3))
    phoneNumberPart1 = ''.join(random.choice(string.digits) for i in range(3))
    phoneNumberPart2 = ''.join(random.choice(string.digits) for i in range(4))
    #return pn.format_number(str(number), pn.PhoneNumberFormat.NATIONAL)
    return '(' + areaCode + ') ' + phoneNumberPart1 + '-' + phoneNumberPart2

def randomInt(numDigis=9):
    maxNumberWithDesiredDigits = pow(10, numDigis) -1
    minNumberWithDesiredDigits = pow(10, numDigis - 1)
    return np.random.randint(minNumberWithDesiredDigits, maxNumberWithDesiredDigits)

def randomStreetAddress():
    return fake.street_name()

def randomStreetAddress2():
    if bool(random.getrandbits(1)):
        return fake.secondary_address()
    return ''

def randomCity():
    return fake.city()

def randomState():
    return fake.state()

def randomZipCode():
    return fake.zipcode()

def generateName(gender=''):
    return fake.name()

def strTimeProp(start, end, format, prop, newformat):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def randomDate(afterDate="1/1/1932 1:30 PM",toDate="1/1/2019 4:50 AM"):
    return strTimeProp(afterDate, toDate, '%m/%d/%Y %I:%M %p', random.random(), "%Y-%m-%d %H:%M:%S")