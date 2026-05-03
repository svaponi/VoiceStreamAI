import asyncio
import datetime
import io
import json
import uuid

import numpy as np
import pydub
import websockets
from TTS.api import TTS

from app.tts.tts_interface import TTSInterface


class Synthesizer(TTSInterface):

    def __init__(self, thread_id=None, **kwargs):
        super().__init__()
        self._tts: TTS | None = None
        self._websocket: websockets | None = None
        thread_id = thread_id or uuid.uuid4().hex
        self.url = "ws://localhost:9127/api/v1/chat/threads/" + thread_id

    @property
    def tts(self) -> TTS:
        if not self._tts:
            self._tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph")
        return self._tts

    async def connect(self) -> websockets:
        if not self._websocket:
            print(f"> Connecting: {self.url}")
            self._websocket = await websockets.connect(self.url)
        return self._websocket

    @property
    def ws(self) -> websockets:
        asyncio.wait_for(self.connect(), timeout=10)
        return self._websocket

    async def ask_ai(self, text: str) -> str:
        ws = await self.connect()
        try:
            payload = {
                "role": "user",
                "content": text,
                "message_id": uuid.uuid4().hex,
                "ts": datetime.datetime.now().isoformat(),
            }
            text = json.dumps(payload)
            print(f"> Sending: {text}")
            await ws.send(text)
            print(f"> Sent: {text}")
            resp = ""
            done = False
            while not done:
                response = await ws.recv()
                response = json.loads(response)
                print(f"< Received: {type(response).__name__} {response}")
                resp += response.get("content")
                done = response.get("done") or False
            return resp
        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    async def synthesize(self, text: str, audio_format="mp3") -> (bytes, str):
        if not text:
            return b""
        text_from_ai = await self.ask_ai(text)
        raw = self.tts.tts(text=text_from_ai, speed=1.2)
        if isinstance(raw, list):
            raw = np.array(raw)
        raw_norm = raw * (32767 / max(0.01, np.max(np.abs(raw))))
        raw_norm = raw_norm.astype(np.int16)
        raw_bytes = raw_norm.tobytes()
        audio = pydub.AudioSegment.from_raw(
            io.BytesIO(raw_bytes), channels=1, sample_width=2, frame_rate=22050
        )
        raw_bytes = audio.export(format=audio_format).read()
        return raw_bytes, text_from_ai
