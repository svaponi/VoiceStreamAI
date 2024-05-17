import json
import os

from .asr_interface import ASRInterface
from .faster_whisper_asr import FasterWhisperASR
from .whisper_asr import WhisperASR


class ASRFactory:
    @staticmethod
    def create_asr_pipeline() -> ASRInterface:
        asr_type = os.getenv("ASR_TYPE", "faster_whisper")
        asr_args = os.getenv("ASR_ARGS") or {}
        if isinstance(asr_args, str):
            try:
                asr_args = json.loads(asr_args)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON arguments: {e}")

        if asr_type == "whisper":
            return WhisperASR(**asr_args)
        if asr_type == "faster_whisper":
            return FasterWhisperASR(**asr_args)
        else:
            raise ValueError(f"Unknown ASR pipeline type: {asr_type}")
