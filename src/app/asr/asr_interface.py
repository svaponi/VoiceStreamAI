import abc
import logging

from app.audio_utils import convert_audio_to_wav

logger = logging.getLogger(__name__)


class ASRInterface(abc.ABC):
    """
    Interface for automatic speech recognition (ASR) systems.
    """

    async def transcribe(self, client):
        """
        Transcribe the given audio data.

        :param client: The client object with all the member variables including the buffer
        :return: The transcription structure, see for example the faster_whisper_asr.py file.
        """

        file_like = await convert_audio_to_wav(client.scratch_buffer)
        language = client.config.get("language")
        to_return = await self._transcribe(file_like, language)
        logger.info("Transcription: %s", to_return)
        return to_return

    @abc.abstractmethod
    async def _transcribe(self, file_like, language=None):
        raise NotImplementedError("This method should be implemented by subclasses.")
