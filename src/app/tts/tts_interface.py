import abc


class TTSInterface(abc.ABC):
    """
    Interface for text-to-speech (TTS).
    """

    @abc.abstractmethod
    async def synthesize(self, text: str, audio_format="mp3") -> (bytes, str):
        """
        Detects voice activity in the given audio data.

        Args:
            client (src.Client): The client to detect on

        Returns:
            List: VAD result, a list of objects containing "start", "end", "confidence"
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
