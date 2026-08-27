import time
import wave
import audioop
import platform
import subprocess

RATE = 44100
CHANNELS = 1
WIDTH = 2
CHUNK_FRAMES = 1024


def record_to_wav(duration, wav_path):
    if platform.system() == "Windows":
        raw, rate, channels = _record_win32(duration)
    else:
        raw, rate, channels = _record_linux(duration)

    if channels > 1:
        raw = audioop.tomono(raw, WIDTH, 0.5, 0.5)
    if rate != RATE:
        raw, _ = audioop.ratecv(raw, WIDTH, 1, rate, RATE, None)

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(WIDTH)
        wf.setframerate(RATE)
        wf.writeframes(raw)


def _record_win32(duration):
    import pyaudiowpatch as pyaudio

    pa = pyaudio.PyAudio()
    stream = None
    try:
        wasapi_info = pa.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_out = pa.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        device = default_out
        for loopback in pa.get_loopback_device_info_generator():
            if default_out["name"] in loopback["name"]:
                device = loopback
                break

        rate = int(device["defaultSampleRate"])
        channels = device["maxInputChannels"]
        frames_needed = int(rate * duration)
        chunks, collected = [], 0

        def _callback(in_data, frame_count, time_info, status):
            nonlocal collected
            chunks.append(in_data)
            collected += frame_count
            done = collected >= frames_needed
            return (None, pyaudio.paComplete if done else pyaudio.paContinue)

        stream = pa.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=device["index"],
            frames_per_buffer=CHUNK_FRAMES,
            stream_callback=_callback,
        )
        stream.start_stream()

        deadline = time.monotonic() + duration + 5
        while stream.is_active() and time.monotonic() < deadline:
            time.sleep(0.05)
    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        pa.terminate()

    return b"".join(chunks), rate, channels


def _record_linux(duration):
    cmd = [
        "parec",
        "--device=@DEFAULT_SINK@.monitor",
        f"--rate={RATE}",
        f"--channels={CHANNELS}",
        "--format=s16le",
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        raw = process.stdout.read(int(RATE * duration) * WIDTH)
    finally:
        process.terminate()
        process.wait()

    return raw, RATE, CHANNELS
