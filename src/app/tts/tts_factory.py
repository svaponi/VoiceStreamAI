import logging

from app.tts.tts import Synthesizer
from app.tts.tts_interface import TTSInterface

logger = logging.getLogger(__name__)


class TTSFactory:

    @staticmethod
    def create_tts() -> TTSInterface:
        return Synthesizer()
