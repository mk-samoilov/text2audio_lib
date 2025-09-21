import numpy as np


class AudioEncoder:
    def __init__(self, sample_rate: int = 44100, frequency_high: int = 2000, frequency_low: int = 1000):
        self.sample_rate = sample_rate
        self.frequency_high = frequency_high
        self.frequency_low = frequency_low
        self.bit_duration = 0.1
        self.silence_duration = 0.05
        
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
    
    def encode_text_to_audio(self, text: str) -> np.ndarray:
        bits = self._text_to_bits(text)
        return self._encode_bits_to_audio(bits)
    
    def encode_bytes_to_audio(self, data: bytes) -> np.ndarray:
        bits = self._bytes_to_bits(data)
        return self._encode_bits_to_audio(bits)
    
    def _encode_bits_to_audio(self, bits: str) -> np.ndarray:
        audio_data = []
        
        for bit in bits:
            if bit == "1":
                tone = self._generate_tone(self.frequency_high, self.bit_duration)
            else:
                tone = self._generate_tone(self.frequency_low, self.bit_duration)
            
            audio_data.append(tone)
            audio_data.append(self._generate_silence(self.silence_duration))
        
        return np.concatenate(audio_data)
    
    def decode_audio_to_text(self, audio_data: np.ndarray) -> str:
        bits = self._decode_audio_to_bits(audio_data)
        return self._bits_to_text(bits)
    
    def decode_audio_to_bytes(self, audio_data: np.ndarray) -> bytes:
        bits = self._decode_audio_to_bits(audio_data)
        return self._bits_to_bytes(bits)
    
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
