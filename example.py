from t2a_lib import encode_bytes_to_audio, decode_audio_to_bytes


def demo_data_encoding():
    print("=== Lib demo ===")
    
    data = b"Hello, World! \x00\x01\x02\x03"
    print(f"Source data: {data}")
    print(f"Data size: {len(data)} bytes")
    
    audio_data, encoder_ = encode_bytes_to_audio(data)
    print(f"Audio data size: {len(audio_data)} samples")
    
    decoded_data = decode_audio_to_bytes(audio_data)
    print(f"Decoded data: {decoded_data}")
    print(f"Data decoded successfully: {data == decoded_data}")
    print()


if __name__ == "__main__":
    demo_data_encoding()
