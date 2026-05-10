#!/usr/bin/env python3
"""Generate realistic-sounding synthetic dog sounds using FM synthesis."""
import wave, struct, math, random, os

SR = 44100
OUTPUT_DIR = "/home/user/Barky1/res/raw"

def write_wav(filename, samples):
    path = os.path.join(OUTPUT_DIR, filename)
    # Normalize to prevent clipping
    peak = max(abs(s) for s in samples) if samples else 1
    scale = 30000 / peak if peak > 0 else 1.0
    clamped = [max(-32767, min(32767, int(s * scale))) for s in samples]
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(struct.pack('<' + 'h' * len(clamped), *clamped))
    print(f"  {filename}: {len(samples)/SR:.2f}s")

def tanh_clip(x, drive=1.5):
    return math.tanh(x * drive) / drive

def osc(freq, t, phase=0.0):
    return math.sin(2 * math.pi * freq * t + phase)

def env_adsr(t, atk, dec, sus, rel, total):
    if t < atk:
        return t / atk if atk > 0 else 1.0
    elif t < atk + dec:
        return 1.0 - (1.0 - sus) * (t - atk) / dec
    elif t < total - rel:
        return sus
    else:
        rem = total - t
        return sus * max(0, rem / rel) if rel > 0 else 0.0

def bark_single(fund, dur, breed_noise=0.12, roughness=30.0, fm_ratio=2.1, fm_depth=3.5):
    """
    Single bark using FM synthesis + roughness modulation + soft clipping.
    fund      - fundamental frequency (Hz)
    dur       - duration (seconds)
    roughness - AM frequency for the 'barky' texture
    fm_ratio  - FM modulator frequency ratio
    fm_depth  - FM modulation index
    """
    n = int(dur * SR)
    samples = []
    mod_freq = fund * fm_ratio

    for i in range(n):
        t = i / SR
        frac = t / dur

        # Pitch glide: sharp initial transient dips then settles
        glide = 1.0 + 0.25 * math.exp(-frac * 18)
        f0 = fund * glide

        # FM modulation index decreases over time (brighter attack)
        idx = fm_depth * math.exp(-frac * 6)

        # Phase modulation (FM synthesis)
        phi_mod = idx * osc(mod_freq * glide, t)

        # Carrier + harmonics
        sig = osc(f0, t, phi_mod) * 0.55
        sig += osc(f0 * 2, t, phi_mod * 0.5) * 0.22
        sig += osc(f0 * 3, t, phi_mod * 0.3) * 0.12
        sig += osc(f0 * 4, t) * 0.06
        sig += osc(f0 * 5, t) * 0.03

        # Breath / noise component
        sig += random.gauss(0, breed_noise)

        # Rough amplitude texture — the "woof" character
        rough = 1.0 + 0.35 * osc(roughness, t) + 0.15 * osc(roughness * 1.7, t)

        # ADSR envelope
        amp = env_adsr(t, 0.008, 0.05, 0.35, dur * 0.25, dur)

        # Soft clip for warmth / naturalness
        out = tanh_clip(sig * rough * amp, drive=1.8)
        samples.append(out * 32000)

    return samples

def silence(dur):
    return [0] * int(dur * SR)

def multi_bark(fund, count, bark_dur, gap, **kw):
    out = []
    for _ in range(count):
        out.extend(bark_single(fund, bark_dur, **kw))
        out.extend(silence(gap))
    return out

def howl(f_start, f_peak, f_end, dur, vibrato_rate=4.5, vibrato_depth=0.015):
    """Sustained howl with smooth pitch arc and vibrato."""
    n = int(dur * SR)
    samples = []
    for i in range(n):
        t = i / SR
        frac = t / dur

        # Smooth pitch arc: rise then fall
        arc = math.sin(math.pi * frac)
        f0 = f_start + (f_peak - f_start) * arc * arc

        # Vibrato kicks in after first 0.3s
        vib_env = max(0, (t - 0.3) / 0.5)
        vib = 1.0 + vibrato_depth * vib_env * math.sin(2 * math.pi * vibrato_rate * t)

        # Pure harmonics, minimal noise — howls are tonal
        sig = osc(f0 * vib, t) * 0.55
        sig += osc(f0 * vib * 2, t) * 0.28
        sig += osc(f0 * vib * 3, t) * 0.10
        sig += osc(f0 * vib * 4, t) * 0.05
        sig += random.gauss(0, 0.015)

        amp = env_adsr(t, 0.18, 0.12, 0.82, 0.4, dur)
        samples.append(tanh_clip(sig * amp, 1.3) * 32000)
    return samples

def growl(fund, dur, mod_rate=14.0, roughness_depth=0.55):
    """Deep guttural growl — heavy sub-harmonic AM + noise."""
    n = int(dur * SR)
    samples = []
    for i in range(n):
        t = i / SR
        frac = t / dur

        # Sub-harmonics dominate in growls
        sig = osc(fund, t) * 0.35
        sig += osc(fund * 0.5, t) * 0.25       # sub-octave
        sig += osc(fund * 1.5, t) * 0.18
        sig += osc(fund * 2, t) * 0.10
        sig += osc(fund * 2.5, t) * 0.06

        # Rough throaty modulation
        rough = 1.0 + roughness_depth * osc(mod_rate, t)
        rough += 0.2 * osc(mod_rate * 0.6, t)

        # Heavy noise floor for growl texture
        sig += random.gauss(0, 0.3)

        amp = env_adsr(t, 0.05, 0.08, 0.75, 0.25, dur)
        out = tanh_clip(sig * rough * amp, 2.2)
        samples.append(out * 32000)
    return samples

def whine(f_start, f_end, dur, tremolo=True):
    """High plaintive whine with descending pitch and emotional tremolo."""
    n = int(dur * SR)
    samples = []
    for i in range(n):
        t = i / SR
        frac = t / dur

        # Pitch descends with a slight bow (starts faster, slows)
        f0 = f_start * ((f_end / f_start) ** (frac * frac))

        # Tremolo for that sad puppy quality
        trem = 1.0 + (0.18 * math.sin(2 * math.pi * 7.5 * t) if tremolo else 0)

        sig = osc(f0, t) * 0.65
        sig += osc(f0 * 2, t) * 0.22
        sig += osc(f0 * 3, t) * 0.08
        sig += random.gauss(0, 0.04)

        amp = env_adsr(t, 0.04, 0.08, 0.65, 0.38, dur)
        samples.append(tanh_clip(sig * trem * amp, 1.2) * 32000)
    return samples

def bay(fund, dur):
    """Beagle-style bay: pitch arc + strong odd harmonics + nasal quality."""
    n = int(dur * SR)
    samples = []
    for i in range(n):
        t = i / SR
        frac = t / dur

        # Bay has two humps in pitch
        arc = math.sin(math.pi * frac * 2) * 0.12
        f0 = fund * (1.0 + arc)

        # Nasal quality: strong odd harmonics
        sig = osc(f0, t) * 0.45
        sig += osc(f0 * 3, t) * 0.30   # strong 3rd = nasal
        sig += osc(f0 * 5, t) * 0.14
        sig += osc(f0 * 2, t) * 0.07
        sig += osc(f0 * 7, t) * 0.05
        sig += random.gauss(0, 0.06)

        rough = 1.0 + 0.2 * osc(22, t)
        amp = env_adsr(t, 0.06, 0.1, 0.7, 0.3, dur)
        samples.append(tanh_clip(sig * rough * amp, 1.6) * 32000)
    return samples

def yips(fund, count):
    """Tiny rapid yips (Pomeranian, etc.) — very short, bright, with pitch bend."""
    out = []
    for _ in range(count):
        dur = 0.10
        n = int(dur * SR)
        for i in range(n):
            t = i / SR
            frac = t / dur
            # Quick pitch drop gives it a "yip" character
            f0 = fund * (1.0 + 0.3 * math.exp(-frac * 20))
            idx = 2.5 * math.exp(-frac * 10)
            phi = idx * osc(f0 * 3, t)
            sig = osc(f0, t, phi) * 0.6
            sig += osc(f0 * 2, t) * 0.25
            sig += random.gauss(0, 0.18)
            amp = env_adsr(t, 0.004, 0.015, 0.3, 0.06, dur)
            out.append(tanh_clip(sig * amp, 2.0) * 32000)
        out.extend(silence(0.09))
    return out

# ── Generate all 18 sounds ────────────────────────────────────────────────────
print("Generating realistic dog sounds...")

# 1. Chihuahua — tiny, yappy, high (3 sharp barks)
write_wav("chihuahua_bark.wav",
    multi_bark(1300, 3, 0.13, 0.09,
               breed_noise=0.22, roughness=45, fm_ratio=2.4, fm_depth=4.0))

# 2. German Shepherd — authoritative, medium-low (2 forceful barks)
write_wav("german_shepherd_bark.wav",
    multi_bark(360, 2, 0.28, 0.14,
               breed_noise=0.10, roughness=28, fm_ratio=2.0, fm_depth=3.8))

# 3. Golden Retriever — warm, friendly (2 open barks)
write_wav("golden_retriever_bark.wav",
    multi_bark(500, 2, 0.24, 0.12,
               breed_noise=0.08, roughness=25, fm_ratio=1.8, fm_depth=3.2))

# 4. Poodle — bright, slightly nasal (4 rapid yaps)
write_wav("poodle_yap.wav",
    multi_bark(820, 4, 0.11, 0.07,
               breed_noise=0.20, roughness=40, fm_ratio=2.3, fm_depth=3.5))

# 5. Bulldog — massive, slow, breathy single woof
write_wav("bulldog_woof.wav",
    bark_single(185, 0.60,
                breed_noise=0.28, roughness=18, fm_ratio=1.5, fm_depth=2.8))

# 6. Husky — melodic, tonal howl
write_wav("husky_howl.wav",
    howl(260, 640, 300, 2.4, vibrato_rate=4.0, vibrato_depth=0.018))

# 7. Beagle — classic long bay
write_wav("beagle_bay.wav",
    bay(440, 1.6))

# 8. Dachshund — persistent, slightly hoarse (5 barks)
write_wav("dachshund_bark.wav",
    multi_bark(620, 5, 0.15, 0.07,
               breed_noise=0.18, roughness=36, fm_ratio=2.1, fm_depth=3.6))

# 9. Labrador — enthusiastic, open-chested (3 barks)
write_wav("labrador_bark.wav",
    multi_bark(470, 3, 0.26, 0.11,
               breed_noise=0.09, roughness=22, fm_ratio=1.9, fm_depth=3.4))

# 10. Rottweiler — deep, rumbling growl
write_wav("rottweiler_growl.wav",
    growl(110, 2.0, mod_rate=12, roughness_depth=0.6))

# 11. Pomeranian — rapid tiny yips
write_wav("pomeranian_yip.wav",
    yips(1550, 6))

# 12. Doberman — sharp, clipped, assertive (2 barks)
write_wav("doberman_bark.wav",
    multi_bark(400, 2, 0.20, 0.11,
               breed_noise=0.12, roughness=32, fm_ratio=2.2, fm_depth=4.2))

# 13. Corgi — medium, herding staccato (4 barks)
write_wav("corgi_bark.wav",
    multi_bark(580, 4, 0.16, 0.08,
               breed_noise=0.14, roughness=30, fm_ratio=2.0, fm_depth=3.3))

# 14. Shih Tzu — small, breathy, slightly husky (3 yaps)
write_wav("shihtzu_yap.wav",
    multi_bark(980, 3, 0.12, 0.08,
               breed_noise=0.30, roughness=42, fm_ratio=2.3, fm_depth=3.0))

# 15. Border Collie — focused, alert (3 crisp barks)
write_wav("border_collie_bark.wav",
    multi_bark(540, 3, 0.19, 0.09,
               breed_noise=0.10, roughness=26, fm_ratio=2.0, fm_depth=3.5))

# 16. Great Dane — very deep, resonant, boomy single woof
write_wav("great_dane_woof.wav",
    bark_single(118, 0.80,
                breed_noise=0.15, roughness=14, fm_ratio=1.4, fm_depth=2.5))

# 17. Puppy — high trembling whine
write_wav("puppy_whine.wav",
    whine(1150, 580, 1.8, tremolo=True))

# 18. Wolf — long dramatic howl
write_wav("wolf_howl.wav",
    howl(195, 490, 220, 3.2, vibrato_rate=3.8, vibrato_depth=0.022))

print(f"\nDone — {len(os.listdir(OUTPUT_DIR))} files in {OUTPUT_DIR}/")
