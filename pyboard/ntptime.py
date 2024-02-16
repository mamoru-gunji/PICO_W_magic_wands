import usocket as socket
try:
    import ustruct as struct
except:
    import struct
import time
    
def ntptime():
    NTP_DELTA = 2208988800
    # NTPサーバー
    ntp_host = "ntp.nict.jp"
    #ntp_host = "time-c.nist.gov"
    #ntp_host = "time.cloudflare.com"
    #ntp_host = "time.google.com"
    
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(ntp_host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

def get_now():
    try:
        t = ntptime()
        t = t + 9*60*60
        datetimetuple = time.gmtime(t)
        print(datetimetuple)
#     year = str(datetimetuple[0])
#     month = zfill(str(datetimetuple[1]),2)
#     mday = zfill(str(datetimetuple[2]),2)
#     hour = zfill(str(datetimetuple[3]),2)
#     minute = zfill(str(datetimetuple[4]),2)
        return datetimetuple
    except OSError:
        return False