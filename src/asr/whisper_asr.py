import os

import numpy as np
from transformers import pipeline

from src.asr.asr_interface import ASRInterface
from src.audio_utils import convert_audio_to_wav


class WhisperASR(ASRInterface):
    def __init__(self, model=None, **kwargs):
        if not model:
            model = os.getenv("OPENAI_WHISPER_MODEL", "openai/whisper-tiny.en")
        self.asr_pipeline = pipeline("automatic-speech-recognition", model=model)

    async def transcribe(self, client):
        file_like = await convert_audio_to_wav(
            client.scratch_buffer
        )

        file_like = np.frombuffer(file_like.read(), dtype=np.int8)

        language = client.config.get("language")
        if language is not None:
            result = self.asr_pipeline(
                file_like, generate_kwargs={"language": language}
            )
        else:
            result = self.asr_pipeline(file_like)

        to_return = {
            "language": "UNSUPPORTED_BY_HUGGINGFACE_WHISPER",
            "language_probability": None,
            "text": result.get("text").strip(),
            "words": "UNSUPPORTED_BY_HUGGINGFACE_WHISPER",
        }
        return to_return
