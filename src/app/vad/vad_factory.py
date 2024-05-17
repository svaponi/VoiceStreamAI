import json
import logging
import os

from app.vad.pyannote_vad import PyannoteVAD
from app.vad.vad_interface import VADInterface

logger = logging.getLogger(__name__)


class VADFactory:

    @staticmethod
    def create_vad_pipeline() -> VADInterface:
        vad_type = os.getenv("VAD_TYPE", "pyannote")
        vad_args = os.getenv("VAD_ARGS") or {}
        if isinstance(vad_args, str):
            try:
                vad_args = json.loads(vad_args)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON arguments: {e}")

        if vad_type == "pyannote":
            return PyannoteVAD(**vad_args)
        else:
            raise ValueError(f"Unknown VAD pipeline type: {vad_type}")
