import re

import weewx

from . import Packet


class OS(object):
    @staticmethod
    def insert_ids(pkt, pkt_type):
        channel = pkt.pop('channel', 0)
        code = pkt.pop('house_code', 0)
        sensor_id = "%s:%s" % (channel, code)
        return Packet.add_identifiers(pkt, sensor_id, pkt_type)


class OSPCR800Packet(Packet):
    # 2016-11-03 04:36:23 : OS : PCR800
    # House Code: 93
    # Channel: 0
    # Battery: OK
    # Rain Rate: 0.0 in/hr
    # Total Rain: 41.0 in

    IDENTIFIER = "PCR800"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Rain Rate':
            ['rain_rate', re.compile(r'([\d.]+) in'), lambda x: float(x)],
        'Total Rain':
            ['rain_total', re.compile(r'([\d.]+) in'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.US
        pkt.update(Packet.parse_lines(lines, OSPCR800Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSPCR800Packet.__name__)

    # {"time" : "2020-06-06 20:15:17", "brand" : "OS", "model" : "Oregon-PCR800", "id" : 32, "channel" : 0, "battery_ok" : 1, "rain_rate_in_h" : 0.150, "rain_in" : 0.082}
    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.US
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery_ok') == 1 else 1
        pkt['rain_rate'] = Packet.get_float(obj, 'rain_rate_in_h')
        pkt['rain_total'] = Packet.get_float(obj, 'rain_in')
        return OS.insert_ids(pkt, OSPCR800Packet.__name__)


# apparently rtl_433 uses BHTR968 when it should be BTHR968
class OSBTHR968Packet(Packet):
    # Added 2017-04-22 ALG
    # 2017-09-12 21:44:55     :       OS :    BHTR968
    # House Code:      111
    # Channel:         0
    # Battery:         OK
    # Celcius:         26.20 C
    # Fahrenheit:      79.16 F
    # Humidity:        36 %
    # Pressure:        1012 mbar

    IDENTIFIER = "BHTR968"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Temperature': ['temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Humidity': ['humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)],
        'Pressure': ['pressure', re.compile(r'([\d.]+) mbar'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSBTHR968Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSBTHR968Packet.__name__)

    # original rtl_433 output
    # {"time" : "2017-01-18 14:56:03", "brand" : "OS", "model" :"BHTR968", "id" : 111, "channel" : 0, "battery" : "OK", "temperature_C" : 27.200, "temperature_F" : 80.960,  "humidity" : 46, "pressure" : 1013}
    # by 06mar2019
    # {"time" : "2019-03-06 13:27:23", "brand" : "OS", "model" : "BHTR968", "id" : 179, "channel" : 0, "battery" : "LOW", "temperature_C" : 19.800, "humidity" : 54, "pressure_hPa" : 974.000}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        if 'pressure' in obj:
            pkt['pressure'] = Packet.get_float(obj, 'pressure_hPa')
        elif 'pressure_hPa' in obj:
            pkt['pressure'] = Packet.get_float(obj, 'pressure_hPa')
        return OS.insert_ids(pkt, OSBTHR968Packet.__name__)


class OSTHGR122NPacket(Packet):
    # 2016-09-12 21:44:55     :       OS :    THGR122N
    # House Code:      96
    # Channel:         3
    # Battery:         OK
    # Temperature:     27.30 C
    # Humidity:        36 %

    IDENTIFIER = "THGR122N"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Temperature': [
            'temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Humidity': ['humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSTHGR122NPacket.PARSEINFO))
        return OS.insert_ids(pkt, OSTHGR122NPacket.__name__)

    # {"time" : "2017-01-18 14:56:03", "brand" : "OS", "model" :"THGR122N", "id" : 211, "channel" : 1, "battery" : "LOW", "temperature_C" : 7.900, "humidity" : 27}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        return OS.insert_ids(pkt, OSTHGR122NPacket.__name__)


class OSTHGR810Packet(Packet):
    # rtl_433 circa jul 2016 emits this
    # 2016-09-01 22:05:47 :Weather Sensor THGR810
    # House Code: 122
    # Channel: 1
    # Battery: OK
    # Celcius: 26.70 C
    # Fahrenheit: 80.06 F
    # Humidity: 58 %

    # rtl_433 circa nov 2016 emits this
    # 2016-11-04 02:21:37 :OS :THGR810
    # House Code: 122
    # Channel: 1
    # Battery: OK
    # Celcius: 22.20 C
    # Fahrenheit: 71.96 F
    # Humidity: 57 %

    IDENTIFIER = "THGR810"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Celcius': [
            'temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Fahrenheit': [
            'temperature_F', re.compile(r'([\d.-]+) F'), lambda x: float(x)],
        'Humidity': ['humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSTHGR810Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSTHGR810Packet.__name__)

    # {"time" : "2020-06-06 20:08:12", "brand" : "OS", "model" : "Oregon-THGR810", "id" : 153, "channel" : 1, "battery_ok" : 1, "temperature_C" : 18.200, "humidity" : 49}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery_ok') == 1 else 1
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        return OS.insert_ids(pkt, OSTHGR810Packet.__name__)


class OSTHR128Packet(Packet):
    # 2019-04-30:   Thermo Sensor THR128
    # House Code:      5
    # Channel:         1
    # Battery:         OK
    # Temperature:     18.800 C

    IDENTIFIER = "OSv1 Temperature Sensor"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Temperature':
            ['temperature', re.compile(r'([\d.-]+) C'), lambda x : float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSTHR128Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSTHR128Packet.__name__)

    # {"time" : "2019-04-30 20:44:00", "brand" : "OS", "model" : "OSv1 Temperature Sensor", "sid" : 5, "channel" : 1, "battery" : "OK", "temperature_C" : 18.800}
    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('sid')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        return OS.insert_ids(pkt, OSTHR128Packet.__name__)


class OSTHR228NPacket(Packet):
    # 2016-09-09 11:59:10 :   Thermo Sensor THR228N
    # House Code:      111
    # Channel:         2
    # Battery:         OK
    # Temperature:     24.70 C

    IDENTIFIER = "Thermo Sensor THR228N"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Temperature':
            ['temperature', re.compile(r'([\d.-]+) C'), lambda x : float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSTHR228NPacket.PARSEINFO))
        return OS.insert_ids(pkt, OSTHR228NPacket.__name__)


class OSUV800Packet(Packet):
    # 2017-01-30 22:00:12 : OS : UV800
    # House Code: 207
    # Channel: 1
    # Battery: OK
    # UV Index: 0

    IDENTIFIER = "UV800"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'UV Index':
            ['uv_index', re.compile(r'([\d.-]+) C'), lambda x : float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSUV800Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSUV800Packet.__name__)

    # {"time" : "2017-01-30 22:19:40", "brand" : "OS", "model" : "UV800", "id" : 207, "channel" : 1, "battery" : "OK", "uv" : 0}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['uv_index'] = Packet.get_float(obj, 'uv')
        return OS.insert_ids(pkt, OSUV800Packet.__name__)


class OSUVR128Packet(Packet):
    # 2019-11-05 07:07:07 : Oregon Scientific UVR128
    # House Code: 116
    # UV Index: 0
    # Battery: OK

    IDENTIFIER = "Oregon Scientific UVR128"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'UV Index': ['uv_index', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSUVR128Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSUVR128Packet.__name__)

    # {"time" : "2019-11-05 07:07:07", "model" : "Oregon Scientific UVR128", "id" : 116, "uv" : 0, "battery" : "OK"}
    # {"time" : "2019-11-19 06:44:53", "model" : "Oregon Scientific UVR128", "id" : 116, "uv" : 0, "battery" : "OK"}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['uv_index'] = Packet.get_float(obj, 'uv')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return OS.insert_ids(pkt, OSUVR128Packet.__name__)


class OSWGR800Packet(Packet):
    # 2016-11-03 04:36:34 : OS : WGR800
    # House Code: 85
    # Channel: 0
    # Battery: OK
    # Gust: 1.1 m/s
    # Average: 1.1 m/s
    # Direction: 22.5 degrees

    IDENTIFIER = "WGR800"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Gust': [
            'wind_gust', re.compile(r'([\d.]+) m'), lambda x: float(x)],
        'Average': [
            'wind_speed', re.compile(r'([\d.]+) m'), lambda x: float(x)],
        'Direction': [
            'wind_dir', re.compile(r'([\d.]+) degrees'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRICWX
        pkt.update(Packet.parse_lines(lines, OSWGR800Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSWGR800Packet.__name__)

    # {"time" : "2020-06-06 21:44:43", "brand" : "OS", "model" : "Oregon-WGR800", "id" : 245, "channel" : 0, "battery_ok" : 1, "wind_max_m_s" : 3.100, "wind_avg_m_s" : 0.000, "wind_dir_deg" : 90.000}
    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery_ok') == 1 else 1
        pkt['wind_gust'] = Packet.get_float(obj, 'wind_max_m_s')
        pkt['wind_speed'] = Packet.get_float(obj, 'wind_avg_m_s')
        pkt['wind_dir'] = Packet.get_float(obj, 'wind_dir_deg')
        return OS.insert_ids(pkt, OSWGR800Packet.__name__)


class OSTHN802Packet(Packet):
    # 2017-08-03 17:24:08     :       OS :    THN802
    # House Code:      157
    # Channel:         3
    # Battery:         OK
    # Celcius:         26.60 C

    IDENTIFIER = "THN802"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Celcius': ['temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSTHN802Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSTHN802Packet.__name__)

    # {"time" : "2017-08-03 17:41:24", "brand" : "OS", "model" : "THN802", "id" : 157, "channel" : 3, "battery" : "OK", "temperature_C" : 26.700}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        return OS.insert_ids(pkt, OSTHN802Packet.__name__)


class OSBTHGN129Packet(Packet):
    # 2017-08-03 17:24:03     :       OS :    BTHGN129
    # House Code:      146
    # Channel:         5
    # Battery:         OK
    # Celcius:         32.00 C
    # Humidity:        50 %
    # Pressure:        959.36 mPa

    IDENTIFIER = "BTHGN129"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Celcius': ['temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Humidity': ['humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)],
        'Pressure': ['pressure', re.compile(r'([\d.]+) mPa'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, OSBTHGN129Packet.PARSEINFO))
        return OS.insert_ids(pkt, OSBTHGN129Packet.__name__)

    # {"time" : "2017-08-03 17:41:48", "brand" : "OS", "model" : "BTHGN129", "id" : 146, "channel" : 5, "battery" : "OK", "temperature_C" : 31.700, "humidity" : 52, "pressure_hPa" : 959.364}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = obj.get('channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['pressure'] = Packet.get_float(obj, 'pressure_hPa')
        return OS.insert_ids(pkt, OSBTHGN129Packet.__name__)


class OSTHGR968Packet(Packet):

    IDENTIFIER = "THGR968"

    # {"time" : "2019-02-15 13:43:25", "brand" : "OS", "model" : "THGR968", "id" : 187, "channel" : 1, "battery" : "OK", "temperature_C" : 16.500, "humidity" : 11}
    # '{"time" : "2019-02-15 13:43:26", "brand" : "OS", "model" : "THGR968", "id" : 187, "channel" : 1, "battery" : "OK", "temperature_C" : 16.500, "humidity" : 11}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = Packet.get_int(obj, 'channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        return OS.insert_ids(pkt, OSTHGR968Packet.__name__)



class OSRGR968Packet(Packet):

    IDENTIFIER = "RGR968"

    # {"time" : "2019-02-15 14:32:51", "brand" : "OS", "model" : "RGR968", "id" : 48, "channel" : 0, "battery" : "OK", "rain_rate" : 0.000, "total_rain" : 6935.100}
    # {"time" : "2019-02-15 14:32:51", "brand" : "OS", "model" : "RGR968", "id" : 48, "channel" : 0, "battery" : "OK", "rain_rate" : 0.000, "total_rain" : 6935.100}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['house_code'] = obj.get('id')
        pkt['channel'] = Packet.get_int(obj, 'channel')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['rain_rate'] = Packet.get_float(obj, 'rain_rate')
        pkt['total_rain'] = Packet.get_float(obj, 'total_rain')
        return OS.insert_ids(pkt, OSRGR968Packet.__name__)
