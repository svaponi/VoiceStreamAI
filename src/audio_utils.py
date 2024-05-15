import io
import wave


async def convert_audio_to_wav(audio_data: bytes):
    """
    Creates a file-like object with the audio data converted ro WAV.
    :return: the file-like object.
    """

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)  # Assuming mono audio
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(audio_data)

    buffer.name = "audio.wav"
    buffer.seek(0)
    return buffer
