from string import ascii_lowercase
from string import ascii_uppercase
import base64
import string
from math import floor
from urllib.parse import urlparse

# Base64 Encoder and Decoder

def toBase64(num, b=64):
    if b <= 0 or b > 64:
        return 0
    base = string.digits + ascii_uppercase + ascii_lowercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res

def toBase10(num, b=64):
    base = string.digits + ascii_uppercase + ascii_lowercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res