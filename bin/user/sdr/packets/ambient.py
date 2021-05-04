import re

import weewx

from . import Packet


class AmbientF007THPacket(Packet):
    # 2017-01-21 18:17:16 : Ambient Weather F007TH Thermo-Hygrometer
    # House Code: 80
    # Channel: 1
    # Temperature: 61.8
    # Humidity: 13 %

#    IDENTIFIER = "Ambient Weather F007TH Thermo-Hygrometer"
    IDENTIFIER = "Ambientweather-F007TH"
    PARSEINFO = {
        'House Code': ['house_code', None, lambda x: int(x)],
        'Channel': ['channel', None, lambda x: int(x)],
        'Temperature': [
            'temperature', re.compile(r'([\d.-]+) F'), lambda x: float(x)],
        'Humidity': ['humidity', re.compile(r'([\d.]+) %'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRIC
        pkt.update(Packet.parse_lines(lines, AmbientF007THPacket.PARSEINFO))
        house_code = pkt.pop('house_code', 0)
        channel = pkt.pop('channel', 0)
        sensor_id = "%s:%s" % (channel, house_code)
        pkt = Packet.add_identifiers(
            pkt, sensor_id, AmbientF007THPacket.__name__)
        return pkt

    # {"time" : "2017-01-21 13:01:30", "model" : "Ambient Weather F007TH Thermo-Hygrometer", "device" : 80, "channel" : 1, "temperature_F" : 61.800, "humidity" : 10}
    # as of 06feb2020:
    # {"time" : "2020-02-05 19:33:11", "model" : "Ambientweather-F007TH", "id" : 201, "channel" : 5, "battery_ok" : 1, "temperature_F" : 39.400, "humidity" : 60, "mic" : "CRC"}

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.US
        house_code = obj.get('device', 0)
        channel = obj.get('channel')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_F')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        sensor_id = "%s:%s" % (channel, house_code)
        pkt = Packet.add_identifiers(
            pkt, sensor_id, AmbientF007THPacket.__name__)
        return pkt


class AmbientWH31EPacket(Packet):

    # {"time" : "2019-02-14 17:24:41.259441", "protocol" : 113, "model" : "AmbientWeather-WH31E", "id" : 24, "channel" : 1, "battery" : "OK", "temperature_C" : 6.000, "humidity" : 42, "data" :"2f00000000", "mic" : "CRC", "mod" : "FSK", "freq1" : 914.984, "freq2" : 914.906, "rssi" : -13.328, "snr" : 13.197, "noise" : -26.525}

    IDENTIFIER = "AmbientWeather-WH31E"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['station_id'] = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['channel'] = Packet.get_int(obj, 'channel')
        pkt['rssi'] = Packet.get_int(obj, 'rssi')
        pkt['snr'] = Packet.get_float(obj, 'snr')
        pkt['noise'] = Packet.get_float(obj, 'noise')
        return AmbientWH31EPacket.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        station_id = pkt.pop('station_id', '0000')
        pkt = Packet.add_identifiers(pkt, station_id, AmbientWH31EPacket.__name__)
        return pkt
