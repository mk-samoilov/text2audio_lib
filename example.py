from t2a_lib import encode_bytes_to_audio, decode_audio_to_bytes, save_audio_to_wav, load_audio_from_wav


def demo_data_encoding():
    print("=== Lib demo ===")
    
    data = b"Hello, World!"
    print(f"Source data: {data}")
    print(f"Data size: {len(data)} bytes")
    
    audio_data, encoder_ = encode_bytes_to_audio(data)
    print(f"Audio data size: {len(audio_data)} samples")

    filename = "encoded_data.wav"
    sample_rate = 44100

    save_audio_to_wav(audio_data, filename, sample_rate)

    file_loaded_audio, _loaded_sample_rate = load_audio_from_wav(filename)
    decoded_data = decode_audio_to_bytes(file_loaded_audio)
    print(f"Decoded data: {decoded_data}")
    print(f"Data decoded successfully: {data == decoded_data}")
    print()


if __name__ == "__main__":
    demo_data_encoding()
