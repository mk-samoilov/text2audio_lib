import os

from t2a_lib import encode_bytes_to_audio, decode_audio_to_bytes, save_audio_to_wav, load_audio_from_wav


def generate_test_data(size_bytes: int) -> bytes:
    return os.urandom(size_bytes)


def test_512kb_ultra_fast():
    print("=== Lib demo for 32KB data ===")
    
    target_size = 32 * 1024
    
    test_data = generate_test_data(target_size)
    
    print("Encoding to audio...")
    audio_data, encoder = encode_bytes_to_audio(test_data)

    print(f"Audio duration: {len(audio_data) / 16000:.2f} seconds")
    
    filename = "32kb_data.wav"
    print(f"\nSaving file ({filename})...")
    save_audio_to_wav(audio_data, filename, 16000)
    
    file_size = os.path.getsize(filename)
    print(f"Audio file size: {file_size / (1024*1024):.2f} МБ")
    
    print("\nЗагрузка и декодирование...")
    loaded_audio, loaded_sample_rate = load_audio_from_wav(filename)
    decoded_data = decode_audio_to_bytes(loaded_audio)

    print(f"Decoded data: {len(decoded_data)} bytes")
    
    is_success = test_data == decoded_data
    print(f"\nResult: {'ok' if is_success else 'error'}")
    
    if not is_success:
        print(f"Expected: {len(test_data)} bytes")
        print(f"Received: {len(decoded_data)} bytes")
        
        if len(test_data) == len(decoded_data):
            differences = sum(1 for a, b in zip(test_data, decoded_data) if a != b)
            print(f"Number of differences: {differences}")


if __name__ == "__main__":
    test_512kb_ultra_fast()
