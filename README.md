# Running on Noise
Wait, you are saying your bluetooth speaker will automatically turn off after being idle for few minutes in order to save power? No worries, the white noise maker will periodically play some white noises for you to keep your bluetooth speaker active!

[Executable](https://github.com/xnsi/running-on-noise/releases/tag/v1.0)

## Attention
This tool is only available for Windows system!

## Dependency
Need [FFmpeg](https://ffmpeg.org/) for playing the noise and creating the Windows tray icon.

## If you do not want to use the executable...
This project uses `pydub` for playing audio. `pydub` is a powerful library but it contains some bugs...

If you just wanna run it as a python script, there's a patch you need to apply to the `_play_with_ffplay` function in `pydub/playback.py`.

```python
@@ -12,6 +12,7 @@
 def _play_with_ffplay(seg):
     PLAYER = get_player_name()
     with NamedTemporaryFile("w+b", suffix=".wav") as f:
+        f.close() # close the file stream
         seg.export(f.name, "wav")
         subprocess.call([PLAYER, "-nodisp", "-autoexit", "-hide_banner", f.name])
```

Need python ≤ 3.12 since `pyaudioop` is removed from 3.13, which is required by `pydub`.
