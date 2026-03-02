import os
import hashlib
import hmac
import secrets
from django.conf import settings
import uuid
from math import radians, cos, sin, asin, sqrt


def generate_barcode():
    return "MDRHC-" + secrets.token_hex(4).upper()


def getlastid(table_name):
    result = table_name.objects.order_by('id').last()
    if result:
        lastid = result.id
        newid = lastid + 1
    else:
        lastid = 0
        newid = 1
    return lastid, newid


def getnewid(table_name):
    result = table_name.objects.order_by('id').last()
    if result:
        newid = result.id + 1
    else:
        newid = 1
    hashid = hashlib.blake2b(str(newid).encode('utf-8'), digest_size=16)
    return newid, hashid.hexdigest()


def getjustnewid(table_name):
    result = table_name.objects.order_by('id').last()
    if result:
        newid = result.id + 1
    else:
        newid = 1
    return newid


def hash_md5(strhash):
    hashed = hashlib.blake2b(strhash.encode('utf-8'), digest_size=16)
    return hashed.hexdigest()


def split_string(string):
    string2 = string.split()
    return string2[0].lower()


def haversine(lat1, lon1, lat2, lon2):
    R = 3959.87433
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    return R * c