import os

from t2a_lib import (encode_bytes_to_audio_compressed, decode_audio_to_bytes_compressed, save_audio_to_wav,
                     load_audio_from_wav, ProtocolConfig)


def generate_test_data(size_bytes: int) -> bytes:
    return os.urandom(size_bytes)


def test_32kb_ultra_compressed():
    print("=== Lib demo for 32KB data with MAXIMUM COMPRESSION ===")
    
    target_size = 32 * 1024
    
    test_data = generate_test_data(target_size)
    print(f"Original data size: {len(test_data)} bytes")
    
    config = ProtocolConfig(
        sample_rate=48000,
        frequency_high=4000,
        frequency_low=500,
        bit_duration=0.001,
        silence_duration=0.0005
    )

    audio_data, encoder, compression_method = encode_bytes_to_audio_compressed(test_data, config, "gzip")
    
    print(f"Compression method used: {compression_method}")
    print(f"Audio duration: {len(audio_data) / config.sample_rate:.2f} seconds")
    
    filename = "32kb_data.wav"
    print(f"\nSaving file ({filename})...")
    save_audio_to_wav(audio_data, filename, config.sample_rate)
    
    file_size = os.path.getsize(filename)
    print(f"Audio file size: {file_size / (1024*1024):.2f} МБ")
    compression_ratio = len(test_data) / file_size
    print(f"Compression ratio: {compression_ratio:.2f}x")
    print(f"Space saved: {((len(test_data) - file_size) / len(test_data) * 100):.1f}%")
    print(f"Efficiency: {file_size / len(test_data) * 100:.1f}% of original size")
    
    print("\nLoading and decoding...")
    loaded_audio, loaded_sample_rate = load_audio_from_wav(filename)
    decoded_data = decode_audio_to_bytes_compressed(loaded_audio, config)

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
    test_32kb_ultra_compressed()
