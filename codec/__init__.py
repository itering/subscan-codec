from scalecodec import ScaleBytes
from scalecodec.base import Singleton
from scalecodec.metadata import MetadataDecoder
from codec.metadata.darwinia import Darwinia78
from codec.metadata.kusama import Kusama1003, Kusama1006, Kusama1008, Kusama1010, Kusama1011, Kusama1012, Kusama1015, \
    Kusama1016, Kusama1017

Decoder = None


class MetadataInstant(metaclass=Singleton):
    Decoder = None


class Darwinia78Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Darwinia78))
            self.Decoder.decode()


class Kusama1003Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1003))
            self.Decoder.decode()


class Kusama1006Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1006))
            self.Decoder.decode()


class Kusama1008Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1008))
            self.Decoder.decode()


class Kusama1010Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1010))
            self.Decoder.decode()


class Kusama1011Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1011))
            self.Decoder.decode()


class Kusama1012Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1012))
            self.Decoder.decode()


class Kusama1015Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1015))
            self.Decoder.decode()


class Kusama1016Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1016))
            self.Decoder.decode()


class Kusama1017Instant(MetadataInstant, metaclass=Singleton):
    Decoder = None

    def __init__(self):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(Kusama1017))
            self.Decoder.decode()
