import asyncio
import configparser
import ctypes
import numpy as np
import os
import pystray
import threading
from concurrent.futures import ThreadPoolExecutor
from scipy.io.wavfile import write
from pydub import AudioSegment, playback
from PIL import Image, ImageDraw

# ---------------- Config ----------------
config = configparser.ConfigParser()
config.read('config.ini')
DURATION = float(config['DEFAULT']['duration'])
INTERVAL = int(config['DEFAULT']['interval'])

SAMPLE_RATE = 44100
AMPLITUDE = 1
NOISE_FILE = "white_noise.wav"

# ---------------- Utilities ----------------
def generate_noise(file, duration, sample_rate=SAMPLE_RATE, amplitude=AMPLITUDE):
    samples = (np.random.normal(0, 1, int(sample_rate * duration)) * amplitude).astype(np.int16)
    write(file, sample_rate, samples)

def get_noise_file():
    if not os.path.isfile(NOISE_FILE):
        generate_noise(NOISE_FILE, DURATION)
    else:
        existing = AudioSegment.from_wav(NOISE_FILE)
        if len(existing) / 1000 != DURATION:
            generate_noise(NOISE_FILE, DURATION)
    return AudioSegment.from_wav(NOISE_FILE)

def is_awake():
    # TODO: improve with real system events
    return ctypes.windll.kernel32.GetTickCount64() != 0

# ---------------- Core ----------------
noise = get_noise_file()
executor = ThreadPoolExecutor()

async def play_noise():
    if is_awake():
        print("Playing white noise...")
        executor.submit(playback.play, noise)

async def timer():
    while True:
        if is_awake():
            await asyncio.sleep(INTERVAL)
            await play_noise()
        else:
            await asyncio.sleep(1)

def exit_action(icon):
    # TODO: not working. use global loop instead.
    # loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    icon.stop()
    os._exit(0)

# ---------------- Tray Icon ----------------
image = Image.new('RGB', (64, 64), 'white')
draw = ImageDraw.Draw(image)
draw.rectangle(
    [(5, 5), (59, 59)],
    fill='white'
)

icon = pystray.Icon(
    "WhiteNoise",
    image,
    "White Noise Maker",
    menu=pystray.Menu(pystray.MenuItem("Exit", exit_action))
)

def main():
    global loop
    threading.Thread(target=icon.run, daemon=True).start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(timer())
    loop.run_forever()

if __name__ == "__main__":
    main()
