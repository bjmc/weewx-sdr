"""Sensor packet subclasses, grouped by manufacturer.

Importing this package pulls in every Packet subclass so that
PacketFactory can discover them and so callers can do
``from user.brands import SomePacket``.
"""

from .acurite import (
    Acurite,
    Acurite00275MPacket,
    Acurite3n1PacketV2,
    Acurite5n1Packet,
    Acurite5n1PacketV2,
    Acurite515Packet,
    Acurite606TXPacket,
    Acurite606TXPacketV2,
    Acurite986Packet,
    AcuriteAtlasPacket,
    AcuriteLightningPacket,
    AcuriteRain899Packet,
    AcuriteTowerPacket,
    AcuriteTowerPacketV2,
    AcuriteWT450Packet,
)
from .alecto import (
    AlectoV1RainPacket,
    AlectoV1TemperaturePacket,
    AlectoV1WindPacket,
)
from .ambient import (
    AmbientF007THPacket,
    AmbientTX8300Packet,
    AmbientWH31BPacket,
    AmbientWH31EPacket,
)
from .auriol import (
    AuriolHG02832Packet,
)
from .bresser import (
    Bresser5in1Packet,
    Bresser6in1Packet,
    Bresser7in1Packet,
    BresserProRainGaugePacket,
)
from .calibeur import (
    CalibeurRF104Packet,
)
from .cotech import (
    Cotech367959Packet,
)
from .ecowitt import (
    EcoWittWH40Packet,
    EcoWittWS68Packet,
)
from .emax import (
    EM3551HPacket,
)
from .esperanza import (
    EsperanzaEWSPacket,
)
from .fine_offset import (
    FOWH0290Packet,
    FOWH2Packet,
    FOWH5Packet,
    FOWH24BPacket,
    FOWH24Packet,
    FOWH25Packet,
    FOWH31LPacket,
    FOWH32BPacket,
    FOWH32Packet,
    FOWH45Packet,
    FOWH51Packet,
    FOWH65BAltPacket,
    FOWH65BPacket,
    FOWH1080Packet,
    FOWH3080Packet,
    FOWHx080Packet,
    FOWS80Packet,
    FOWS90Packet,
)
from .hideki import (
    Hideki,
    HidekiRainPacket,
    HidekiTS04Packet,
    HidekiWindPacket,
)
from .holman import (
    HolmanWS5029Packet,
)
from .infactory import (
    InFactoryTHPacket,
)
from .kedsum import (
    KedsumTHPacket,
)
from .lacrosse import (
    LaCrosseBreezeProPacket,
    LaCrosseLTVR3Packet,
    LaCrosseTX18Packet,
    LaCrosseTX141Bv3Packet,
    LaCrosseTX141THBv2Packet,
    LaCrosseTXPacket,
    LaCrosseWSPacket,
)
from .nexus import (
    NexusTemperaturePacket,
)
from .oregon_scientific import (
    OS,
    OSBTHGN129Packet,
    OSBTHR918Packet,
    OSBTHR968Packet,
    OSPCR800Packet,
    OSRGR968Packet,
    OSTHGR122NPacket,
    OSTHGR810Packet,
    OSTHGR968Packet,
    OSTHN802Packet,
    OSTHR128Packet,
    OSTHR228NPacket,
    OSUV800Packet,
    OSUVR128Packet,
    OSWGR800Packet,
)
from .prologue import (
    ProloguePacket,
    PrologueTHPacket,
)
from .rubicson import (
    RubicsonTempPacket,
    RubicsonTempPacketV2,
)
from .springfield import (
    SpringfieldTMPacket,
)
from .tfa import (
    TFADropPacket,
    TFATwinPlus303049Packet,
)
from .tsft002 import (
    TSFT002Packet,
)
from .vevor import (
    Vevor7in1Packet,
)
from .ws2032 import (
    WS2032Packet,
)
from .wt0124 import (
    WT0124Packet,
)

__all__ = [
    'Acurite',
    'Acurite00275MPacket',
    'Acurite3n1PacketV2',
    'Acurite515Packet',
    'Acurite5n1Packet',
    'Acurite5n1PacketV2',
    'Acurite606TXPacket',
    'Acurite606TXPacketV2',
    'Acurite986Packet',
    'AcuriteAtlasPacket',
    'AcuriteLightningPacket',
    'AcuriteRain899Packet',
    'AcuriteTowerPacket',
    'AcuriteTowerPacketV2',
    'AcuriteWT450Packet',
    'AlectoV1RainPacket',
    'AlectoV1TemperaturePacket',
    'AlectoV1WindPacket',
    'AmbientF007THPacket',
    'AmbientTX8300Packet',
    'AmbientWH31BPacket',
    'AmbientWH31EPacket',
    'AuriolHG02832Packet',
    'Bresser5in1Packet',
    'Bresser6in1Packet',
    'Bresser7in1Packet',
    'BresserProRainGaugePacket',
    'CalibeurRF104Packet',
    'Cotech367959Packet',
    'EM3551HPacket',
    'EcoWittWH40Packet',
    'EcoWittWS68Packet',
    'EsperanzaEWSPacket',
    'FOWH0290Packet',
    'FOWH1080Packet',
    'FOWH24BPacket',
    'FOWH24Packet',
    'FOWH25Packet',
    'FOWH2Packet',
    'FOWH3080Packet',
    'FOWH31LPacket',
    'FOWH32BPacket',
    'FOWH32Packet',
    'FOWH45Packet',
    'FOWH51Packet',
    'FOWH5Packet',
    'FOWH65BAltPacket',
    'FOWH65BPacket',
    'FOWHx080Packet',
    'FOWS80Packet',
    'FOWS90Packet',
    'Hideki',
    'HidekiRainPacket',
    'HidekiTS04Packet',
    'HidekiWindPacket',
    'HolmanWS5029Packet',
    'InFactoryTHPacket',
    'KedsumTHPacket',
    'LaCrosseBreezeProPacket',
    'LaCrosseLTVR3Packet',
    'LaCrosseTX141Bv3Packet',
    'LaCrosseTX141THBv2Packet',
    'LaCrosseTX18Packet',
    'LaCrosseTXPacket',
    'LaCrosseWSPacket',
    'NexusTemperaturePacket',
    'OS',
    'OSBTHGN129Packet',
    'OSBTHR918Packet',
    'OSBTHR968Packet',
    'OSPCR800Packet',
    'OSRGR968Packet',
    'OSTHGR122NPacket',
    'OSTHGR810Packet',
    'OSTHGR968Packet',
    'OSTHN802Packet',
    'OSTHR128Packet',
    'OSTHR228NPacket',
    'OSUV800Packet',
    'OSUVR128Packet',
    'OSWGR800Packet',
    'ProloguePacket',
    'PrologueTHPacket',
    'RubicsonTempPacket',
    'RubicsonTempPacketV2',
    'SpringfieldTMPacket',
    'TFADropPacket',
    'TFATwinPlus303049Packet',
    'TSFT002Packet',
    'Vevor7in1Packet',
    'WS2032Packet',
    'WT0124Packet',
]
