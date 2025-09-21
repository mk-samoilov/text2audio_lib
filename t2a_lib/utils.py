import numpy as np

from scipy.io import wavfile

from typing import Tuple


def save_audio_to_wav(audio_data: np.ndarray, filename: str, sample_rate: int = 44100) -> None:
    if audio_data.dtype != np.int16:
        audio_data = (audio_data * 32767).astype(np.int16)
    
    wavfile.write(filename, sample_rate, audio_data)


def load_audio_from_wav(filename: str) -> Tuple[np.ndarray, int]:
    sample_rate, audio_data = wavfile.read(filename)
    
    if audio_data.dtype == np.int16:
        audio_data = audio_data.astype(np.float32) / 32767.0
    elif audio_data.dtype == np.int32:
        audio_data = audio_data.astype(np.float32) / 2147483647.0
    elif audio_data.dtype == np.uint8:
        audio_data = (audio_data.astype(np.float32) - 128) / 128.0
    
    return audio_data, sample_rate


def normalize_audio(audio_data: np.ndarray) -> np.ndarray:
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        return audio_data / max_val
    return audio_data


def convert_to_mono(audio_data: np.ndarray) -> np.ndarray:
    if len(audio_data.shape) > 1:
        return np.mean(audio_data, axis=1)
    return audio_data
