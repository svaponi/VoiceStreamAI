import os

import numpy as np
from transformers import pipeline

from app.asr.asr_interface import ASRInterface


class WhisperASR(ASRInterface):
    def __init__(self, model=None, **kwargs):
        if not model:
            model = os.getenv("OPENAI_WHISPER_MODEL", "openai/whisper-tiny.en")
        self.asr_pipeline = pipeline("automatic-speech-recognition", model=model)

    async def _transcribe(self, file_like, language=None):
        file_like = np.frombuffer(file_like.read(), dtype=np.int8)

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
