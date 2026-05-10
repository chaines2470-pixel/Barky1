#!/usr/bin/env python3
"""Generate synthetic dog sounds as WAV files."""
import wave, struct, math, random, os

SAMPLE_RATE = 44100
OUTPUT_DIR = "/home/user/Barky1/res/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_wav(filename, samples):
    path = os.path.join(OUTPUT_DIR, filename)
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        data = struct.pack('<' + 'h' * len(samples), *samples)
        f.writeframes(data)
    print(f"  {filename}: {len(samples)/SAMPLE_RATE:.2f}s")

def clamp(v):
    return max(-32767, min(32767, int(v)))

def adsr(t, attack, decay, sustain, release, total):
    if t < attack:
        return t / attack
    elif t < attack + decay:
        return 1.0 - (1.0 - sustain) * (t - attack) / decay
    elif t < total - release:
        return sustain
    else:
        rem = total - t
        return sustain * rem / release if rem > 0 else 0

def noise():
    return random.uniform(-1, 1)

def sine(freq, t):
    return math.sin(2 * math.pi * freq * t)

def make_bark(freq, dur, amplitude=28000, harmonics=3, noise_mix=0.15):
    """Single bark sound."""
    samples = []
    n = int(dur * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        env = adsr(t, 0.01, 0.05, 0.4, 0.1, dur)
        sig = sine(freq, t)
        for h in range(2, harmonics + 1):
            sig += sine(freq * h, t) * (0.5 / h)
        sig = sig / (1 + harmonics * 0.3)
        sig = sig * (1 - noise_mix) + noise() * noise_mix
        samples.append(clamp(sig * env * amplitude))
    return samples

def make_multi_bark(freq, count, bark_dur, gap_dur, **kwargs):
    """Multiple barks with gaps."""
    all_samples = []
    for _ in range(count):
        all_samples.extend(make_bark(freq, bark_dur, **kwargs))
        gap = int(gap_dur * SAMPLE_RATE)
        all_samples.extend([0] * gap)
    return all_samples

def make_howl(start_freq, end_freq, dur, amplitude=26000):
    """Frequency-sweep howl."""
    samples = []
    n = int(dur * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        frac = t / dur
        freq = start_freq + (end_freq - start_freq) * math.sin(math.pi * frac)
        env = adsr(t, 0.15, 0.1, 0.8, 0.3, dur)
        sig = sine(freq, t) * 0.7 + sine(freq * 2, t) * 0.2 + sine(freq * 3, t) * 0.1
        samples.append(clamp(sig * env * amplitude))
    return samples

def make_growl(freq, dur, amplitude=25000):
    """Low growl with heavy noise."""
    samples = []
    n = int(dur * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        env = adsr(t, 0.05, 0.1, 0.7, 0.2, dur)
        # Rough growl: low freq + lots of noise + harmonics
        sig = sine(freq, t) * 0.4
        sig += sine(freq * 1.5, t) * 0.2
        sig += noise() * 0.4
        # Modulate amplitude slightly for roughness
        mod = 0.85 + 0.15 * sine(18, t)
        samples.append(clamp(sig * mod * env * amplitude))
    return samples

def make_whine(start_freq, end_freq, dur, amplitude=22000):
    """Descending whine."""
    samples = []
    n = int(dur * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        frac = t / dur
        freq = start_freq - (start_freq - end_freq) * frac
        env = adsr(t, 0.05, 0.1, 0.6, 0.4, dur)
        # Add slight vibrato
        vibrato = 1 + 0.02 * sine(6, t)
        sig = sine(freq * vibrato, t) * 0.8 + sine(freq * vibrato * 2, t) * 0.2
        samples.append(clamp(sig * env * amplitude))
    return samples

def make_yips(freq, count, amplitude=24000):
    """Short high-pitched yips."""
    all_samples = []
    for _ in range(count):
        n = int(0.12 * SAMPLE_RATE)
        for i in range(n):
            t = i / SAMPLE_RATE
            env = adsr(t, 0.005, 0.02, 0.3, 0.06, 0.12)
            # Slight pitch drop in each yip
            f = freq * (1.0 - 0.1 * t / 0.12)
            sig = sine(f, t) * 0.7 + sine(f * 2, t) * 0.2 + noise() * 0.1
            all_samples.append(clamp(sig * env * amplitude))
        gap = int(0.08 * SAMPLE_RATE)
        all_samples.extend([0] * gap)
    return all_samples

def make_bay(freq, dur, amplitude=27000):
    """Beagle-style baying - melodic with frequency modulation."""
    samples = []
    n = int(dur * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        env = adsr(t, 0.08, 0.1, 0.65, 0.25, dur)
        # Bay has a distinctive pitch rise then fall
        sweep = 1 + 0.15 * math.sin(math.pi * t / dur)
        sig = sine(freq * sweep, t) * 0.6
        sig += sine(freq * sweep * 1.5, t) * 0.25
        sig += sine(freq * sweep * 2, t) * 0.15
        sig += noise() * 0.05
        samples.append(clamp(sig * env * amplitude))
    return samples

print("Generating dog sounds...")

# 1. Chihuahua - tiny high-pitched bark (3 rapid barks)
write_wav("chihuahua_bark.wav",
    make_multi_bark(1400, 3, 0.12, 0.08, amplitude=22000, harmonics=2, noise_mix=0.2))

# 2. German Shepherd - authoritative medium-low bark (2 barks)
write_wav("german_shepherd_bark.wav",
    make_multi_bark(380, 2, 0.22, 0.12, amplitude=30000, harmonics=4, noise_mix=0.18))

# 3. Golden Retriever - friendly medium bark (2 barks)
write_wav("golden_retriever_bark.wav",
    make_multi_bark(520, 2, 0.2, 0.1, amplitude=28000, harmonics=3, noise_mix=0.15))

# 4. Poodle - yappy medium-high bark (4 barks)
write_wav("poodle_yap.wav",
    make_multi_bark(900, 4, 0.1, 0.07, amplitude=23000, harmonics=2, noise_mix=0.2))

# 5. Bulldog - heavy low woof (1 big woof)
write_wav("bulldog_woof.wav",
    make_bark(200, 0.5, amplitude=31000, harmonics=5, noise_mix=0.25))

# 6. Husky - melodic howl (rises and falls)
write_wav("husky_howl.wav",
    make_howl(280, 680, 2.2, amplitude=26000))

# 7. Beagle - baying sound
write_wav("beagle_bay.wav",
    make_bay(460, 1.4, amplitude=27000))

# 8. Dachshund - persistent medium barks (5 barks)
write_wav("dachshund_bark.wav",
    make_multi_bark(650, 5, 0.14, 0.06, amplitude=24000, harmonics=3, noise_mix=0.15))

# 9. Labrador - enthusiastic medium barks (3 barks)
write_wav("labrador_bark.wav",
    make_multi_bark(490, 3, 0.2, 0.1, amplitude=29000, harmonics=3, noise_mix=0.16))

# 10. Rottweiler - deep growl
write_wav("rottweiler_growl.wav",
    make_growl(120, 1.8, amplitude=30000))

# 11. Pomeranian - tiny rapid yips
write_wav("pomeranian_yip.wav",
    make_yips(1600, 5, amplitude=20000))

# 12. Doberman - sharp assertive bark (2 barks)
write_wav("doberman_bark.wav",
    make_multi_bark(420, 2, 0.18, 0.1, amplitude=30000, harmonics=3, noise_mix=0.2))

# 13. Corgi - herding bark (4 barks, medium)
write_wav("corgi_bark.wav",
    make_multi_bark(600, 4, 0.15, 0.08, amplitude=26000, harmonics=3, noise_mix=0.15))

# 14. Shih Tzu - breathy high yap (3 yaps)
write_wav("shihtzu_yap.wav",
    make_multi_bark(1100, 3, 0.1, 0.07, amplitude=20000, harmonics=2, noise_mix=0.3))

# 15. Border Collie - alert medium bark (3 barks)
write_wav("border_collie_bark.wav",
    make_multi_bark(560, 3, 0.17, 0.09, amplitude=27000, harmonics=3, noise_mix=0.14))

# 16. Great Dane - very deep resonant woof (1 big woof)
write_wav("great_dane_woof.wav",
    make_bark(130, 0.7, amplitude=32000, harmonics=5, noise_mix=0.2))

# 17. Puppy - high plaintive whine
write_wav("puppy_whine.wav",
    make_whine(1200, 600, 1.5, amplitude=22000))

# 18. Wolf - dramatic long howl
write_wav("wolf_howl.wav",
    make_howl(220, 520, 3.0, amplitude=28000))

print(f"\nAll sounds saved to {OUTPUT_DIR}/")
print(f"Total: {len(os.listdir(OUTPUT_DIR))} files")
