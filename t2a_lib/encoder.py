import numpy as np

import gzip
import lzma
import bz2
import zlib


class AudioEncoder:
    def __init__(self, sample_rate: int = 22050, frequency_high: int = 2400, frequency_low: int = 800, bit_duration: float = 0.02, silence_duration: float = 0.01):
        self.sample_rate = sample_rate
        self.frequency_high = frequency_high
        self.frequency_low = frequency_low
        self.bit_duration = bit_duration
        self.silence_duration = silence_duration
        
    @staticmethod
    def _text_to_bits(text: str) -> str:
        return "".join(format(ord(char), "08b") for char in text)
    
    @staticmethod
    def _bytes_to_bits(data: bytes) -> str:
        return "".join(format(byte, "08b") for byte in data)
    
    @staticmethod
    def _bits_to_text(bits: str) -> str:
        text = ""
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    @staticmethod
    def _bits_to_bytes(bits: str) -> bytes:
        data = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                data.append(int(byte, 2))
        return bytes(data)
    
    def _generate_tone(self, frequency: int, duration: float) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return np.sin(2 * np.pi * frequency * t)
    
    def _generate_silence(self, duration: float) -> np.ndarray:
        return np.zeros(int(self.sample_rate * duration))
    
    @staticmethod
    def _compress_data(data: bytes, method: str = "gzip") -> bytes:
        if method == "gzip":
            return gzip.compress(data)
        elif method == "lzma":
            return lzma.compress(data)
        elif method == "bz2":
            return bz2.compress(data)
        elif method == "zlib":
            return zlib.compress(data)
        else:
            raise ValueError(f"Неподдерживаемый метод сжатия: {method}")
    
    @staticmethod
    def _decompress_data(compressed_data: bytes, method: str = "gzip") -> bytes:
        if method == "gzip":
            return gzip.decompress(compressed_data)
        elif method == "lzma":
            return lzma.decompress(compressed_data)
        elif method == "bz2":
            return bz2.decompress(compressed_data)
        elif method == "zlib":
            return zlib.decompress(compressed_data)
        else:
            raise ValueError(f"Неподдерживаемый метод сжатия: {method}")
    
    @staticmethod
    def _get_best_compression_method(data: bytes) -> tuple:
        methods = ["gzip", "lzma", "bz2", "zlib"]
        best_method = "gzip"
        best_ratio = 1.0
        
        for method in methods:
            try:
                compressed = AudioEncoder._compress_data(data, method)
                ratio = len(compressed) / len(data)
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_method = method
            except:
                continue
                
        return best_method, best_ratio
    
    def encode_text_to_audio(self, text: str) -> np.ndarray:
        bits = self._text_to_bits(text)
        return self._encode_bits_to_audio(bits)
    
    def encode_bytes_to_audio(self, data: bytes) -> np.ndarray:
        bits = self._bytes_to_bits(data)
        return self._encode_bits_to_audio(bits)
    
    def encode_bytes_to_audio_compressed(self, data: bytes, compression_method: str = None) -> tuple:
        if compression_method is None:
            compression_method, ratio = self._get_best_compression_method(data)
        
        compressed_data = self._compress_data(data, compression_method)
        
        method_header = compression_method.encode("utf-8")
        method_header_len = len(method_header).to_bytes(4, "big")
        
        full_data = method_header_len + method_header + compressed_data
        bits = self._bytes_to_bits(full_data)
        audio_data = self._encode_bits_to_audio(bits)
        
        return audio_data, compression_method
    
    def _encode_bits_to_audio(self, bits: str) -> np.ndarray:
        chunk_size = 1000
        audio_chunks = []
        
        for i in range(0, len(bits), chunk_size):
            bit_chunk = bits[i:i+chunk_size]
            chunk_audio = []
            
            for bit in bit_chunk:
                if bit == "1":
                    tone = self._generate_tone(self.frequency_high, self.bit_duration)
                else:
                    tone = self._generate_tone(self.frequency_low, self.bit_duration)
                
                chunk_audio.append(tone)
                chunk_audio.append(self._generate_silence(self.silence_duration))
            
            if chunk_audio:
                audio_chunks.append(np.concatenate(chunk_audio))
        
        return np.concatenate(audio_chunks)
    
    def decode_audio_to_text(self, audio_data: np.ndarray) -> str:
        bits = self._decode_audio_to_bits(audio_data)
        return self._bits_to_text(bits)
    
    def decode_audio_to_bytes(self, audio_data: np.ndarray) -> bytes:
        bits = self._decode_audio_to_bits(audio_data)
        return self._bits_to_bytes(bits)
    
    def decode_audio_to_bytes_compressed(self, audio_data: np.ndarray) -> bytes:
        bits = self._decode_audio_to_bits(audio_data)
        full_data = self._bits_to_bytes(bits)
        
        if len(full_data) < 4:
            raise ValueError("Недостаточно данных для декодирования")
        
        method_header_len = int.from_bytes(full_data[:4], "big")
        if len(full_data) < 4 + method_header_len:
            raise ValueError("Недостаточно данных для метода сжатия")
        
        compression_method = full_data[4:4+method_header_len].decode("utf-8")
        compressed_data = full_data[4+method_header_len:]
        
        original_data = self._decompress_data(compressed_data, compression_method)
        return original_data
    
    def _decode_audio_to_bits(self, audio_data: np.ndarray) -> str:
        bits = ""
        chunk_size = int(self.sample_rate * (self.bit_duration + self.silence_duration))
        
        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i+chunk_size]
            if len(chunk) < chunk_size:
                break
                
            tone_chunk = chunk[:int(self.sample_rate * self.bit_duration)]
            
            fft = np.fft.fft(tone_chunk)
            fre_ = np.fft.fftfreq(len(tone_chunk), 1/self.sample_rate)
            
            high_power = np.abs(fft[np.abs(fre_ - self.frequency_high).argmin()])
            low_power = np.abs(fft[np.abs(fre_ - self.frequency_low).argmin()])
            
            if high_power > low_power:
                bits += "1"
            else:
                bits += "0"
        
        return bits
