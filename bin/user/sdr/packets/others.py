import re

import weewx

from . import Packet
from .hideki import Hideki


class Bresser5in1Packet(Packet):
    #  'time' => '2018-12-15 16:04:04',
    #  'model' => 'Bresser-5in1',
    #  'id' => 118,
    #  'temperature_C' => 6.4000000000000003552713678800500929355621337890625,
    #  'humidity' => 87,
    #  'wind_gust' => 2.79999999999999982236431605997495353221893310546875,
    #  'wind_speed' => 2.899999999999999911182158029987476766109466552734375,
    #  'wind_dir_deg' => 315,
    #  'rain_mm' => 10.800000000000000710542735760100185871124267578125,
    #  'data' => 'e7897fd71fd6ef9bff78f7feff18768028e02910640087080100',
    #  'mic' => 'CHECKSUM',

    # {"time" : "2018-12-15 16:04:04", "model" : "Bresser-5in1", "id" : 118,
    # "temperature_C" : 6.400, "humidity" : 87, "wind_gust" : 2.800,
    # "wind_speed" : 2.900, "wind_dir_deg" : 315.000, "rain_mm" : 10.800,
    # "data" : "e7897fd71fd6ef9bff78f7feff18768028e02910640087080100",
    # "mic" : "CHECKSUM"}#012

    IDENTIFIER = "Bresser-5in1"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['wind_dir'] = Packet.get_float(obj, 'wind_dir_deg')
        pkt['uv'] = Packet.get_float(obj, 'uv')
        pkt['uv_index'] = Packet.get_float(obj, 'uvi')
        # deal with different labels from rtl_433
        for dst, src in [('wind_speed', 'wind_speed_ms'),
                         ('gust_speed', 'gust_speed_ms'),
                         ('rain_total', 'rainfall_mm'),
                         ('wind_speed', 'wind_speed'),
                         ('gust_speed', 'gust_speed'),
                         ('rain_total', 'rain_mm')]:
            if src in obj:
                pkt[dst] = Packet.get_float(obj, src)
        return Bresser5in1Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        pkt = Packet.add_identifiers(pkt, station_id, Bresser5in1Packet.__name__)
        return pkt


class CalibeurRF104Packet(Packet):
    # 2016-11-01 01:25:28 :Calibeur RF-104
    # ID: 1
    # Temperature: 1.8 C
    # Humidity: 71 %

    # 2016-11-04 05:16:39 :Calibeur RF-104
    # ID: 1
    # Temperature: -2.2 C
    # Humidity: 71 %

    IDENTIFIER = "Calibeur RF-104"
    PARSEINFO = {
        'ID': ['id', None, lambda x: int(x)],
        'Temperature': [
            'temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Humidity': ['humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, CalibeurRF104Packet.PARSEINFO))
        pkt_id = pkt.pop('id', 0)
        sensor_id = "%s" % pkt_id
        pkt = Packet.add_identifiers(
            pkt, sensor_id, CalibeurRF104Packet.__name__)
        return pkt


class EcoWittWH40Packet(Packet):
    # This is for a WH40 rain sensor

    # {"time" : "2020-02-05 12:37:05", "model" : "EcoWitt-WH40", "id" : 52591, "rain_mm" : 0.800, "data" : "0002ed0000", "mic" : "CRC"}

    IDENTIFIER = "EcoWitt-WH40"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['station_id'] = obj.get('id')
        pkt['rain_total'] = Packet.get_float(obj, 'rain_mm')
        return EcoWittWH40Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', 0)
        return Packet.add_identifiers(pkt, station_id, EcoWittWH40Packet.__name__)


class HolmanWS5029Packet(Packet):
    # {"time" : "2019-08-07 10:35:07", "model" : "Holman Industries WS5029 weather station", "id" : 53761, "temperature_C" : 9.100, "humidity" : 102, "rain_mm" : 39.500, "wind_avg_km_h" : 0, "direction_deg" : 338}

    IDENTIFIER = "Holman Industries WS5029 weather station"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['wind_dir'] = Packet.get_float(obj, 'direction_deg')
        pkt['wind_speed'] = Packet.get_float(obj, 'wind_avg_km_h')
        pkt['rain_total'] = Packet.get_float(obj, 'rain_mm')
        return HolmanWS5029Packet.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        return Packet.add_identifiers(pkt, station_id, HolmanWS5029Packet.__name__)


class ProloguePacket(Packet):
    # 2017-03-19 : Prologue Temperature and Humidity Sensor
    # {"time" : "2017-03-15 20:14:19", "model" : "Prologue sensor", "id" : 5, "rid" : 166, "channel" : 1, "battery" : "OK", "button" : 0, "temperature_C" : -0.700, "humidity" : 49}

    IDENTIFIER = "Prologue sensor"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        sensor_id = obj.get('rid')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['channel'] = obj.get('channel')
        pkt = Packet.add_identifiers(pkt, sensor_id, ProloguePacket.__name__)
        return pkt


class RubicsonTempPacket(Packet):
    # 2017-01-15 14:49:03 : Rubicson Temperature Sensor
    # House Code: 14
    # Channel: 1
    # Battery: OK
    # Temperature: 4.5 C
    # CRC: OK

    IDENTIFIER = "Rubicson Temperature Sensor"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Battery': ['battery', None, lambda x: 0 if x == 'OK' else 1],
        'Temperature': ['temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, RubicsonTempPacket.PARSEINFO))
        channel = pkt.pop('channel', 0)
        code = pkt.pop('house_code', 0)
        sensor_id = "%s:%s" % (channel, code)
        return Packet.add_identifiers(pkt, sensor_id, RubicsonTempPacket.__name__)

    # {"time" : "2017-01-17 20:47:41", "model" : "Rubicson Temperature Sensor", "id" : 14, "channel" : 1, "battery" : "OK", "temperature_C" : -1.800, "crc" : "OK"}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        channel = obj.get('channel', 0)
        code = obj.get('id', 0)
        sensor_id = "%s:%s" % (channel, code)
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return Packet.add_identifiers(pkt, sensor_id, RubicsonTempPacket.__name__)



class SpringfieldTMPacket(Packet):
    # {"time" : "2019-01-20 11:14:00", "model" : "Springfield Temperature & Moisture", "sid" : 224, "channel" : 3, "battery" : "OK", "transmit" : "MANUAL", "temperature_C" : -204.800, "moisture" : 0, "mic" : "CHECKSUM"}

    IDENTIFIER = "Springfield Temperature & Moisture"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        sensor_id = obj.get('sid')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['moisture'] = Packet.get_float(obj, 'moisture')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['channel'] = obj.get('channel')
        pkt['transmit'] = obj.get('transmit')
        pkt = Packet.add_identifiers(pkt, sensor_id, SpringfieldTMPacket.__name__)
        return pkt


class TFATwinPlus303049Packet(Packet):
    # 2019-09-25 17:15:12 :   TFA-Twin-Plus-30.3049
    # Channel: 1
    # Battery: OK
    # Temperature: 8.40 C
    # Humidity: 91 %

    # {"time" : "2019-09-25 17:15:12", "model" : "TFA-Twin-Plus-30.3049", "id" : 13, "channel" : 1, "battery" : "OK", "temperature_C" : 8.400, "humidity" : 91, "mic" : "CHECK  SUM"}

    IDENTIFIER = "TFA-Twin-Plus-30.3049"
    PARSEINFO = {
        'Rolling Code': ['rolling_code', None, lambda x: int(x)],
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
        pkt.update(Packet.parse_lines(lines, TFATwinPlus303049Packet.PARSEINFO))
        return Hideki.insert_ids(pkt, TFATwinPlus303049Packet.__name__)

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['rolling_code'] = obj.get('rc')
        pkt['channel'] = obj.get('channel')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        return Hideki.insert_ids(pkt, TFATwinPlus303049Packet.__name__)


class TSFT002Packet(Packet):
    # time : 2019-12-22 16:57:58
    # model : TS-FT002 Id : 127
    # Depth : 186 Temperature: 20.9 C Transmit Interval: 180 Battery Flag?: 8 MIC : CHECKSUM

    # {"time" : "2019-12-22 22:54:58", "model" : "TS-FT002", "id" : 127, "depth_cm" : 186, "temperature_C" : 20.700, "transmit_s" : 180, "flags" : 8, "mic" : "CHECKSUM"}

    IDENTIFIER = "TS-FT002"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['depth'] = Packet.get_float(obj, 'depth_cm')
        pkt['transmit'] = Packet.get_float(obj, 'transmit_s')
        pkt['flags'] = Packet.get_int(obj, 'transmit_s')
        sensor_id = pkt.pop('id', '0000')
        pkt = Packet.add_identifiers(pkt, sensor_id, TSFT002Packet.__name__)
        return pkt


class WT0124Packet(Packet):
    # 2019-04-23: WT0124 Pool Thermometer
    # {"time" : "2019-04-23 12:28:52", "model" : "WT0124 Pool Thermometer", "rid" : 122, "channel" : 1, "temperature_C" : 22.800, "mic" : "CHECKSUM", "data" : 172}

    IDENTIFIER = "WT0124 Pool Thermometer"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        sensor_id = obj.get('rid')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt = Packet.add_identifiers(pkt, sensor_id, WT0124Packet.__name__)
        return pkt
