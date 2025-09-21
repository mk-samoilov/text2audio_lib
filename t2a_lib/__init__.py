from .encoder import AudioEncoder
from .protocol_conf import ProtocolConfig
from .utils import save_audio_to_wav, load_audio_from_wav, normalize_audio, convert_to_mono


def create_encoder(config: ProtocolConfig = None) -> AudioEncoder:
    if config:
        return AudioEncoder(
            sample_rate=config.sample_rate,
            frequency_high=config.frequency_high,
            frequency_low=config.frequency_low,
            bit_duration=config.bit_duration,
            silence_duration=config.silence_duration
        )

    return AudioEncoder()


def encode_text_to_audio(text: str, config: ProtocolConfig = None) -> tuple:
    encoder_ = create_encoder(config)
    audio_data = encoder_.encode_text_to_audio(text)
    return audio_data, encoder_


def decode_audio_to_text(audio_data, config: ProtocolConfig = None) -> str:
    encoder_ = create_encoder(config)
    return encoder_.decode_audio_to_text(audio_data)


def encode_bytes_to_audio(data: bytes, config: ProtocolConfig = None) -> tuple:
    encoder_ = create_encoder(config)
    audio_data = encoder_.encode_bytes_to_audio(data)
    return audio_data, encoder_


def decode_audio_to_bytes(audio_data, config: ProtocolConfig = None) -> bytes:
    encoder_ = create_encoder(config)
    return encoder_.decode_audio_to_bytes(audio_data)


__all__ = [
    "AudioEncoder",
    "ProtocolConfig",
    "create_encoder",
    "encode_text_to_audio",
    "decode_audio_to_text",
    "encode_bytes_to_audio",
    "decode_audio_to_bytes",
    "save_audio_to_wav",
    "load_audio_from_wav",
    "normalize_audio",
    "convert_to_mono"
]
