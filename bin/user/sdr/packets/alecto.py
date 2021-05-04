import weewx

from . import Packet


class AlectoV1TemperaturePacket(Packet):
    # {"time" : "2018-08-29 17:07:34", "model" : "AlectoV1 Temperature Sensor", "id" : 88, "channel" : 2, "battery" : "OK", "temperature_C" : 27.700, "humidity" : 42, "mic" : "CHECKSUM"}

    IDENTIFIER = "AlectoV1 Temperature Sensor"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC
        station_id = obj.get('id')
        pkt['temperature'] = Packet.get_float(obj, 'temperature_C')
        pkt['humidity'] = Packet.get_float(obj, 'humidity')
        pkt = Packet.add_identifiers(pkt, station_id, AlectoV1TemperaturePacket.__name__)
        return pkt


class AlectoV1WindPacket(Packet):
    # {"time" : "2019-01-20 11:14:00", "model" : "AlectoV1 Wind Sensor", "id" : 7, "channel" : 0, "battery" : "OK", "wind_speed" : 0.000, "wind_gust" : 0.000, "wind_direction" : 270, "mic" : "CHECKSUM"}

    IDENTIFIER = "AlectoV1 Wind Sensor"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC  # FIXME: units have not been verified
        station_id = obj.get('id')
        pkt['wind_speed'] = Packet.get_float(obj, 'wind_speed')
        pkt['wind_gust'] = Packet.get_float(obj, 'wind_gust')
        pkt['wind_dir'] = Packet.get_int(obj, 'wind_direction')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['channel'] = obj.get('channel')
        pkt = Packet.add_identifiers(pkt, station_id, AlectoV1WindPacket.__name__)
        return pkt


class AlectoV1RainPacket(Packet):
    # {"time" : "2019-01-20 15:29:21", "model" : "AlectoV1 Rain Sensor", "id" : 13, "channel" : 0, "battery" : "OK", "rain_total" : 15.500, "mic" : "CHECKSUM"}

    IDENTIFIER = "AlectoV1 Rain Sensor"

    @staticmethod
    def parse_json(obj):
        pkt = dict()
        pkt['dateTime'] = Packet.parse_time(obj.get('time'))
        pkt['usUnits'] = weewx.METRIC # FIXME: units have not been verified
        station_id = obj.get('id')
        pkt['rain_total'] = Packet.get_float(obj, 'rain_total')
        pkt['battery'] = 0 if obj.get('battery') == 'OK' else 1
        pkt['channel'] = obj.get('channel')
        pkt = Packet.add_identifiers(pkt, station_id, AlectoV1RainPacket.__name__)
        return pkt
