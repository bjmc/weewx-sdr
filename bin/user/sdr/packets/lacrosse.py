import re

import weewx

from . import Packet


class LaCrosseWSPacket(Packet):
    # 2016-09-08 00:43:52 :LaCrosse WS :9 :202
    # Temperature: 21.0 C
    # 2016-09-08 00:43:53 :LaCrosse WS :9 :202
    # Humidity: 92
    # 2016-09-08 00:43:53 :LaCrosse WS :9 :202
    # Wind speed: 0.0 m/s
    # Direction: 67.500
    # 2016-11-03 17:43:20 :LaCrosse WS :9 :202
    # Rainfall: 850.04 mm

    # {"time" : "2016-11-04 14:42:49", "model" : "LaCrosse WS", "ws_id" : 9, "id" : 202, "temperature_C" : 12.100}
    # {"time" : "2016-11-04 14:44:58", "model" : "LaCrosse WS", "ws_id" : 9, "id" : 202, "humidity" : 67}
    # {"time" : "2016-11-04 14:49:16", "model" : "LaCrosse WS", "ws_id" : 9, "id" : 202, "wind_speed_ms" : 0.800, "wind_direction" : 270.000}

    IDENTIFIER = "LaCrosse WS"
    PARSEINFO = {
        'Wind speed': [
            'wind_speed', re.compile(r'([\d.]+) m/s'), lambda x: float(x)],
        'Direction': ['wind_dir', None, lambda x: float(x)],
        'Temperature': [
            'temperature', re.compile(r'([\d.-]+) C'), lambda x: float(x)],
        'Humidity': ['humidity', None, lambda x: int(x)],
        'Rainfall': [
            'rain_total', re.compile(r'([\d.]+) mm'), lambda x: float(x)]}

    @staticmethod
    def parse_text(ts, payload, lines):
        pkt = dict()
        pkt['dateTime'] = ts
        pkt['usUnits'] = weewx.METRICWX
        pkt.update(Packet.parse_lines(lines, LaCrosseWSPacket.PARSEINFO))
        parts = payload.split(':')
        if len(parts) == 3:
            pkt['ws_id'] = parts[1].strip()
            pkt['hw_id'] = parts[2].strip()
        return LaCrosseWSPacket.insert_ids(pkt)

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRICWX
        pkt['ws_id'] = obj.get('ws_id')
        pkt['hw_id'] = obj.get('id')
        if 'temperature_C' in obj:
            pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        if 'humidity' in obj:
            pkt['humidity'] = Packet.get_float(obj, 'humidity')
        if 'wind_speed_ms' in obj:
            pkt['wind_speed'] = Packet.get_float(obj, 'wind_speed_ms')
        if 'wind_direction' in obj:
            pkt['wind_dir'] = Packet.get_float(obj, 'wind_direction')
        if 'rain' in obj:
            pkt['rain_total'] = Packet.get_float(obj, 'rain')
        return LaCrosseWSPacket.insert_ids(pkt)

    @staticmethod
    def insert_ids(pkt):
        ws_id = pkt.pop('ws_id', 0)
        hardware_id = pkt.pop('hw_id', 0)
        sensor_id = "%s:%s" % (ws_id, hardware_id)
        pkt = Packet.add_identifiers(pkt, sensor_id, LaCrosseWSPacket.__name__)
        return pkt


class LaCrosseTX141THBv2Packet(Packet):

    # {"time" : "2017-01-16 15:24:43", "temperature" : 54.140, "humidity" : 34, "id" : 221, "model" : "LaCrosse TX141TH-Bv2 sensor", "battery" : "OK", "test" : "Yes"}

    IDENTIFIER = "LaCrosse TX141TH-Bv2 sensor"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.US
        sensor_id = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt = Packet.add_identifiers(pkt, sensor_id, LaCrosseTX141THBv2Packet.__name__)
        return pkt


class LaCrosseTXPacket(Packet):

    # {"time" : "2017-07-30 21:11:19", "model" : "LaCrosse TX Sensor", "id" : 127, "humidity" : 34.000}
    # {"time" : "2017-07-30 21:11:19", "model" : "LaCrosse TX Sensor", "id" : 127, "temperature_C" : 27.100}

    IDENTIFIER = "LaCrosse TX Sensor"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        sensor_id = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt = Packet.add_identifiers(pkt, sensor_id, LaCrosseTXPacket.__name__)
        return pkt
