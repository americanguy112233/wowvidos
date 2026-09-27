import sys
import runpy
import urllib.error

sys.argv = [
    "voice.py",
    "build/vo",
    "build/voice.wav",
    "--engine",
    "elevenlabs"
]

try:
    runpy.run_path("voice.py", run_name="__main__")
except urllib.error.HTTPError as error:
    print("\nHTTP:", error.code)
    print("SERVER RESPONSE:")
    print(error.read().decode("utf-8", errors="replace"))