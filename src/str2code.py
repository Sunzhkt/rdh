import re


def str_encode(s, rule='utf-8'):
    sc = s.encode(rule)
    bc = [bin(ii)[2:].rjust(8, '0') for ii in sc]
    return ''.join(bc)


def str_decode(s, rule='utf-8'):
    if len(s) == 0:
        print("error, none to decode!")
        return
    elif len(s) % 8 != 0:
        s = s.ljust(len(s) + 8 - len(s) % 8, '0')
    msg = re.sub(r'0x', '', hex(int(s, 2)))
    try:
        return bytes.fromhex(msg).decode(rule)
    except:
        return msg
        pass
