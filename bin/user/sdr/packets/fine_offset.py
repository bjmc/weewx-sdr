import re

import weewx

from . import Packet


class FOWH1080Packet(Packet):
    # 2016-09-02 22:26:05 :Fine Offset WH1080 weather station
    # Msg type: 0
    # StationID: 0026
    # Temperature: 19.9 C
    # Humidity: 78 %
    # Wind string: E
    # Wind degrees: 90
    # Wind avg speed: 0.00
    # Wind gust: 1.22
    # Total rainfall: 144.3
    # Battery: OK

    # {"time" : "2016-11-04 14:40:38", "model" : "Fine Offset WH1080 weather station", "msg_type" : 0, "id" : 38, "temperature_C" : 12.500, "humidity" : 68, "direction_str" : "E", "direction_deg" : "90", "speed" : 8.568, "gust" : 12.240, "rain" : 249.600, "battery" : "OK"}

    # this assumes rain total is in mm
    # this assumes wind speed is kph

    IDENTIFIER = "Fine Offset WH1080 weather station"
    PARSEINFO = {
#        'Msg type': ['msg_type', None, None],
        'StationID': ['station_id', None, None],
        'Temperature': [
            'temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Humidity': [
            'humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)],
#        'Wind string': ['wind_dir_ord', None, None],
        'Wind degrees': ['wind_dir', None, lambda x: int(x)],
        'Wind avg speed': ['wind_speed', None, lambda x: float(x)],
        'Wind gust': ['wind_gust', None, lambda x: float(x)],
        'Total rainfall': ['rain_total', None, lambda x: float(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, FOWH1080Packet.PARSEINFO))
        return FOWH1080Packet.insert_ids(pkt)

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['station_id'] = obj.get('id')
        pkt['msg_type'] = Packet.get_int(obj, 'msg_type')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['wind_dir'] = Packet.get_float(obj, 'direction_deg')
        pkt['wind_speed'] = Packet.get_float(obj, 'speed')
        pkt['wind_gust'] = Packet.get_float(obj, 'gust')
        rain_total = Packet.get_float(obj, 'rain')
        if rain_total is not None:
            pkt['rain_total'] = rain_total / 10.0 # convert to cm
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return FOWH1080Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH1080Packet.__name__)


class FOWHx080Packet(Packet):
    # 2017-05-15 11:58:31: Fine Offset Electronics WH1080 / WH3080 Weather Station
    # Msg type: 0
    # Station ID: 236
    # Temperature: 23.9 C
    # Humidity: 48%
    # Wind string: NE
    # Wind degrees: 45
    # Wind Avg Speed: 1.22
    # Wind gust: 2.45
    # Total rainfall: 525.3
    # Battery: OK

    # 2017-05-15 12:04:48: Fine Offset Electronics WH1080 / WH3080 Weather Station
    # Msg type: 1
    # Station ID: 173
    # Signal Type: WWVB / MSF
    # Hours: 21
    # Minutes: 71
    # Seconds: 11
    # Year: 2165
    # Month: 25
    # Day: 70

    # apparently there are different identifiers for the same packet, depending
    # on which version of rtl_433 is running.  one version has extra spaces,
    # while another version does not.  so for now, and until rtl_433
    # stabilizes, match on something unique to these packets that still matches
    # the strings from different rtl_433 versions.

    # this assumes rain total is in mm (as of dec 2019)
    # this assumes wind speed is kph (as of dec 2019)

    #IDENTIFIER = "Fine Offset Electronics WH1080 / WH3080 Weather Station"
    #IDENTIFIER = "Fine Offset Electronics WH1080/WH3080 Weather Station"
    IDENTIFIER = "Fine Offset Electronics WH1080"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        # older versions of rlt_433 user 'station_id'
        if 'station_id' in obj:
            pkt['station_id'] = obj.get('station_id')
        # but some newer versions of rtl_433 seem to use 'id'
        if 'id' in obj:
            pkt['station_id'] = obj.get('id')
        pkt['msg_type'] = Packet.get_int(obj, 'msg_type')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['wind_dir'] = Packet.get_float(obj, 'direction_deg')
        pkt['wind_speed'] = Packet.get_float(obj, 'speed')
        pkt['wind_gust'] = Packet.get_float(obj, 'gust')
        rain_total = Packet.get_float(obj, 'rain')
        if rain_total is not None:
            pkt['rain_total'] = rain_total / 10.0 # convert to cm
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['signal_type'] = 1 if obj.get('signal_type') == 'WWVB / MSF' else 0
        pkt['hours'] = Packet.get_int(obj, 'hours')
        pkt['minutes'] = Packet.get_int(obj, 'minutes')
        pkt['seconds'] = Packet.get_int(obj, 'seconds')
        pkt['year'] = Packet.get_int(obj, 'year')
        pkt['month'] = Packet.get_int(obj, 'month')
        pkt['day'] = Packet.get_int(obj, 'day')
        return FOWHx080Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWHx080Packet.__name__)


class FOWH3080Packet(Packet):
    # 2017-05-15 11:58:08: Fine Offset Electronics WH3080 Weather Station
    # Msg type: 2
    # UV Sensor ID: 225
    # Sensor Status: OK
    # UV Index: 8
    # Lux: 120160.5
    # Watts / m: 175.93
    # Foot-candles: 11167.33

    # {"time" : "2017-05-15 17:21:07", "model" : "Fine Offset Electronics WH3080 Weather Station", "msg_type" : 2, "uv_sensor_id" : 225, "uv_status" : "OK", "uv_index" : 1, "lux" : 7837.000, "wm" : 11.474, "fc" : 728.346}

    IDENTIFIER = "Fine Offset Electronics WH3080 Weather Station"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['station_id'] = obj.get('uv_sensor_id')
        pkt['msg_type'] = Packet.get_int(obj, 'msg_type')
        pkt['uv_index'] = Packet.get_float(obj, 'uv_index')
        pkt['luminosity'] = Packet.get_float(obj, 'lux')
        pkt['radiation'] = Packet.get_float(obj, 'wm')
        pkt['illumination'] = Packet.get_float(obj, 'fc')
        pkt['uv_status'] = 0 if obj.get('uv_status') == 'OK' else 1
        return FOWH3080Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH3080Packet.__name__)


class FOWH24Packet(Packet):
    # This is for a WH24 which is the sensor array for several station models

    # {"time" : "2019-02-11 03:44:32", "model" : "Fine Offset WH24", "id" : 140, "temperature_C" : 12.600, "humidity" : 80, "wind_dir_deg" : 111, "wind_speed_ms" : 0.280, "gust_speed_ms" : 1.120, "rainfall_mm" : 1150.800, "uv" : 1, "uvi" : 0, "light_lux" : 0.000, "battery" : "OK", "mic" : "CRC"}
    # {"time" : "2019-02-11 03:44:48", "model" : "Fine Offset WH24", "id" : 140, "temperature_C" : 12.600, "humidity" : 80, "wind_dir_deg" : 109, "wind_speed_ms" : 0.980, "gust_speed_ms" : 1.120, "rainfall_mm" : 1150.800, "uv" : 1, "uvi" : 0, "light_lux" : 0.000, "battery" : "OK", "mic" : "CRC"}

    IDENTIFIER = "Fine Offset WH24"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['wind_dir'] = Packet.get_float(obj, 'wind_dir_deg')
        pkt['wind_speed'] = Packet.get_float(obj, 'wind_speed_ms')
        pkt['wind_gust'] = Packet.get_float(obj, 'gust_speed_ms')
        pkt['rain_total'] = Packet.get_float(obj, 'rainfall_mm')
        pkt['uv_index'] = Packet.get_float(obj, 'uvi')
        pkt['light'] = Packet.get_float(obj, 'light_lux')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return FOWH24Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH24Packet.__name__)


class FOWH25Packet(Packet):
    # 2016-09-02 22:26:05 :   Fine Offset Electronics, WH25
    # ID:     239
    # Temperature: 19.9 C
    # Humidity: 78 %
    # Pressure: 1007.9 hPa
    #
    # 2018-10-09 19:45:12 :   Fine Offset Electronics, WH25
    # id : 21
    # temperature_C : 20.900
    # humidity : 65
    # pressure_hPa : 980.400
    # battery : OK
    # mic : CHECKSUM

    # {"time" : "2017-03-25 05:33:57", "model" : "Fine Offset Electronics, WH25", "id" : 239, "temperature_C" : 30.200, "humidity" : 68, "pressure" : 1008.000}
    # {"time" : "2018-10-10 13:37:11", "model" : "Fine Offset Electronics, WH25", "id" : 21, "temperature_C" : 21.600, "humidity" : 66, "pressure_hPa" : 972.800, "battery" : "OK", "mic" : "CHECKSUM"}
    IDENTIFIER = "Fine Offset Electronics, WH25"
    PARSEINFO = {
        'ID': ['station_id', None, lambda x: int(x)],
        'Temperature':
            ['temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Humidity': ['humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)],
        'Pressure':
            ['pressure', re.compile(r'([\d.-]+) hPa'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, FOWH25Packet.PARSEINFO))
        return FOWH25Packet.insert_ids(pkt)

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['pressure'] = Packet.get_float(obj, 'pressure_hPa')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return FOWH25Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH25Packet.__name__)


class FOWH2Packet(Packet):
    # {"time" : "2018-08-29 17:08:33", "model" : "Fine Offset Electronics, WH2 Temperature/Humidity sensor", "id" : 129, "temperature_C" : 24.200, "mic" : "CRC"}

    IDENTIFIER = "Fine Offset Electronics, WH2"
    PARSEINFO = {
        'ID': ['station_id', None, lambda x: int(x)],
        'Temperature':
            ['temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)]
        }

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, FOWH2Packet.PARSEINFO))
        return FOWH2Packet.insert_ids(pkt)

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        return FOWH2Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH2Packet.__name__)


class FOWH32BPacket(Packet):
    # This is for a WH32B which is the indoors sensor array for an Ambient
    # Weather WS-2902A. The same sensor array is used for several models.

    # time      : 2019-04-08 00:48:02
    # model     : Fineoffset-WH32B
    # ID        : 146
    # Temperature: 17.5 C
    # Humidity  : 60 %
    # Pressure  : 1001.2 hPa
    # Battery   : OK
    # Integrity : CHECKSUM

    # {"time" : "2019-04-08 07:06:03", "model" : "Fineoffset-WH32B", "id" : 146, "temperature_C" : 16.900, "humidity" : 59, "pressure_hPa" : 1001.300, "battery" : "OK", "mic" : "CHECKSUM"}

    IDENTIFIER = "Fineoffset-WH32B"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['pressure'] = Packet.get_float(obj, 'pressure_hPa')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return FOWH32BPacket.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH32BPacket.__name__)


class FOWH5Packet(Packet):
    # {"time" : "2019-10-27 14:51:21", "model" : "Fine Offset WH5 sensor", "id" : 48, "temperature_C" : 11.700, "humidity" : 62, "mic" : "CRC"}

    IDENTIFIER = "Fine Offset WH5 sensor"
    PARSEINFO = {
        'ID': ['station_id', None, lambda x: int(x)],
        'Temperature': ['temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)]
    }

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, FOWH5Packet.PARSEINFO))
        return FOWH5Packet.insert_ids(pkt)

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        return FOWH5Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH5Packet.__name__)


class FOWH65BPacket(Packet):
    # This is for a WH65B which is the sensor array for an Ambient Weather
    # WS-2902A. The same sensor array is used for several models.

    # 2018-10-10 13:37:02 :   Fine Offset WH65B
    # id : 89
    # temperature_C : 17.600
    # humidity : 93
    # wind_dir_deg : 224
    # wind_speed_ms : 1.540
    # gust_speed_ms : 2.240
    # rainfall_mm : 325.500
    # uv : 130
    # uvi : 0
    # light_lux : 13454.000
    # battery : OK
    # mic : CRC

    # {"time" : "2018-10-10 13:37:02", "model" : "Fine Offset WH65B", "id" : 89, "temperature_C" : 17.600, "humidity" : 93, "wind_dir_deg" : 224, "wind_speed_ms" : 1.540, "gust_speed_ms" : 2.240, "rainfall_mm" : 325.500, "uv" : 130, "uvi" : 0, "light_lux" : 13454.000, "battery" : "OK", "mic" : "CRC"}
    IDENTIFIER = "Fine Offset WH65B"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['wind_dir'] = Packet.get_float(obj, 'wind_dir_deg')
        pkt['wind_speed'] = Packet.get_float(obj, 'wind_speed_ms')
        pkt['wind_gust'] = Packet.get_float(obj, 'gust_speed_ms')
        pkt['rain_total'] = Packet.get_float(obj, 'rainfall_mm')
        pkt['uv'] = Packet.get_float(obj, 'uv')
        pkt['uv_index'] = Packet.get_float(obj, 'uvi')
        pkt['light'] = Packet.get_float(obj, 'light_lux')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return FOWH65BPacket.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH65BPacket.__name__)

class FOWH0290Packet(Packet):
    # This is for a WH0290 Air Quality Monitor (Ambient Weather PM25)

    #{"time" : "@0.084044s", "model" : "Fine Offset Electronics, WH0290", "id" : 204, "pm2_5_ug_m3" : 9, "pm10_0_ug_m3" : 10, "mic" : "CHECKSUM"}

    IDENTIFIER = "Fine Offset Electronics, WH0290"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['usUnits'] = weewx.METRIC
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['station_id'] = obj.get('id')
        pkt['pm2_5_atm'] = Packet.get_float(obj, 'pm2_5_ug_m3')
        pkt['pm10_0_atm'] = Packet.get_float(obj, 'pm10_0_ug_m3')
        return FOWH0290Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, FOWH0290Packet.__name__)
