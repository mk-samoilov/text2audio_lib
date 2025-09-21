# Text2Audio Library

Библиотека для кодирования текста и байтов в аудио сигналы и их декодирования.

## Возможности

- Кодирование текста в аудио сигнал
- Кодирование байтов в аудио сигнал  
- Декодирование аудио обратно в текст или байты
- Сохранение и загрузка аудио файлов
- Настраиваемые параметры кодирования
- Поддержка пользовательских конфигураций

## Установка

```bash
pip install -r requirements.txt
```

## Использование

### Базовое использование

```python
from t2a_lib import encode_text_to_audio, decode_audio_to_text

# Кодирование текста в аудио
text = "Привет, мир!"
audio_data, encoder = encode_text_to_audio(text)

# Декодирование аудио обратно в текст
decoded_text = decode_audio_to_text(audio_data)
print(decoded_text)  # "Привет, мир!"
```

### Работа с байтами

```python
from t2a_lib import encode_bytes_to_audio, decode_audio_to_bytes

# Кодирование байтов в аудио
data = b"Hello, World!"
audio_data, encoder = encode_bytes_to_audio(data)

# Декодирование аудио обратно в байты
decoded_data = decode_audio_to_bytes(audio_data)
print(decoded_data)  # b"Hello, World!"
```

### Работа с файлами

```python
from t2a_lib import save_text_to_wav, load_text_from_wav

# Сохранение текста в WAV файл
save_text_to_wav("Привет, мир!", "output.wav")

# Загрузка текста из WAV файла
text = load_text_from_wav("output.wav")
print(text)  # "Привет, мир!"
```

### Пользовательская конфигурация

```python
from t2a_lib import AudioEncoder, ProtocolConfig

# Создание пользовательской конфигурации
config = ProtocolConfig(
    sample_rate=22050,
    frequency_high=3000,
    frequency_low=500,
    bit_duration=0.2,
    silence_duration=0.1
)

# Использование с пользовательской конфигурацией
encoder = AudioEncoder(
    sample_rate=config.sample_rate,
    frequency_high=config.frequency_high,
    frequency_low=config.frequency_low
)

audio_data = encoder.encode_text_to_audio("Тест")
decoded_text = encoder.decode_audio_to_text(audio_data)
```

## Параметры конфигурации

- `sample_rate`: Частота дискретизации (по умолчанию: 44100 Гц)
- `frequency_high`: Частота для бита '1' (по умолчанию: 2000 Гц)
- `frequency_low`: Частота для бита '0' (по умолчанию: 1000 Гц)
- `bit_duration`: Длительность одного бита (по умолчанию: 0.1 сек)
- `silence_duration`: Длительность паузы между битами (по умолчанию: 0.05 сек)

## Запуск демонстрации

```bash
python main.py
```

## Принцип работы

Библиотека использует частотную модуляцию для кодирования данных:
- Бит '1' кодируется высокочастотным тоном
- Бит '0' кодируется низкочастотным тоном
- Между битами добавляются паузы для разделения
- Декодирование происходит через анализ частотного спектра
