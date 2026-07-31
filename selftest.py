"""Smoke test for the Deepgram half — no microphone, hotkey or macOS permission needed.

Synthesises speech with the macOS `say` command, streams it as 16 kHz mono PCM frames
through the same Transcriber the real path uses, and prints the transcript. Only a
Deepgram key is required. This separates "the cloud config is wrong" from "permissions
or the microphone are wrong", which is the first fork in almost every bug report.

    .venv/bin/python selftest.py
    .venv/bin/python selftest.py "Schedule a discovery call for next Tuesday"
"""
import asyncio
import os
import subprocess
import sys
import tempfile
import wave

import config
import macos
from deepgram_live import Transcriber

DEFAULT_PHRASE = "Schedule a discovery call for next Tuesday at three pm"


def synth_pcm(text):
    """macOS `say` -> 16 kHz mono 16-bit PCM. The WAV header is stripped via `wave`."""
    with tempfile.TemporaryDirectory() as d:
        aiff = os.path.join(d, "s.aiff")
        wav = os.path.join(d, "s.wav")
        subprocess.run(["say", "-o", aiff, text], check=True)
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1",
                        aiff, wav], check=True)
        with wave.open(wav, "rb") as w:
            assert w.getframerate() == config.SAMPLE_RATE and w.getnchannels() == 1
            return w.readframes(w.getnframes())


async def run(text):
    key = macos.get_api_key()
    if not key:
        print("No Deepgram key found (Keychain or environment). See the README.",
              file=sys.stderr)
        sys.exit(1)
    pcm = synth_pcm(text)
    frame = config.BLOCKSIZE * 2  # bytes per frame (int16)
    # `say` speaks English, so pin the recogniser to English regardless of the
    # configured dictation language — otherwise a mismatch looks like a broken key.
    t = Transcriber(key, "en")
    for i in range(0, len(pcm), frame):
        t.send(pcm[i:i + frame])   # buffered in the queue until start()
    await t.start()
    heard = await t.finish()
    print(f"SAID:   {text}")
    print(f"HEARD:  {heard or '(nothing)'}")
    print("-> the Deepgram path works" if heard
          else "-> no finals came back; check the key and the parameters")


if __name__ == "__main__":
    phrase = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PHRASE
    asyncio.run(run(phrase))
