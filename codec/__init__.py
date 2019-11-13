from scalecodec import ScaleBytes
from abc import ABC
from scalecodec.metadata import MetadataDecoder


class MetadataInstant(ABC):
    Decoder = None

    def __init__(self, metadata):
        if self.Decoder is None:
            self.Decoder = MetadataDecoder(ScaleBytes(metadata))
            self.Decoder.decode()
