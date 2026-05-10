#!/usr/bin/env python3
"""Generate cute dog icon for Barky app."""
from PIL import Image, ImageDraw
import math, os

def draw_dog_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    cx, cy = s // 2, s // 2

    # Background circle (warm orange gradient approximation)
    for r in range(s // 2, 0, -1):
        frac = 1.0 - r / (s // 2)
        rc = int(255 * (1 - frac * 0.1))
        gc = int(107 + frac * 20)
        bc = int(53 - frac * 10)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(rc, gc, bc, 255))

    def sc(v):
        return int(v * s / 192)

    # Ears (floppy)
    ear_color = (139, 90, 43)
    ear_shadow = (110, 70, 30)
    # Left ear
    d.ellipse([sc(28), sc(36), sc(82), sc(108)], fill=ear_shadow)
    d.ellipse([sc(32), sc(32), sc(78), sc(104)], fill=ear_color)
    # Right ear
    d.ellipse([sc(110), sc(36), sc(164), sc(108)], fill=ear_shadow)
    d.ellipse([sc(114), sc(32), sc(160), sc(104)], fill=ear_color)

    # Head (tan/cream)
    head_color = (222, 184, 135)
    head_dark = (195, 158, 110)
    d.ellipse([sc(38), sc(44), sc(154), sc(160)], fill=head_dark)
    d.ellipse([sc(34), sc(40), sc(150), sc(156)], fill=head_color)

    # White muzzle area
    muzzle_color = (245, 230, 210)
    d.ellipse([sc(62), sc(100), sc(130), sc(158)], fill=muzzle_color)

    # Eyes
    eye_white = (255, 255, 255)
    eye_brown = (80, 40, 15)
    eye_shine = (255, 255, 255)
    eye_dark = (30, 15, 5)

    # Left eye
    d.ellipse([sc(54), sc(70), sc(84), sc(100)], fill=eye_white)
    d.ellipse([sc(60), sc(75), sc(80), sc(96)], fill=eye_brown)
    d.ellipse([sc(63), sc(77), sc(77), sc(93)], fill=eye_dark)
    d.ellipse([sc(67), sc(79), sc(73), sc(85)], fill=eye_shine)

    # Right eye
    d.ellipse([sc(108), sc(70), sc(138), sc(100)], fill=eye_white)
    d.ellipse([sc(112), sc(75), sc(132), sc(96)], fill=eye_brown)
    d.ellipse([sc(115), sc(77), sc(129), sc(93)], fill=eye_dark)
    d.ellipse([sc(119), sc(79), sc(125), sc(85)], fill=eye_shine)

    # Eyebrows (expressive)
    brow_color = (139, 90, 43)
    d.ellipse([sc(54), sc(62), sc(84), sc(74)], fill=brow_color)
    d.ellipse([sc(56), sc(64), sc(82), sc(72)], fill=head_color)
    d.ellipse([sc(108), sc(62), sc(138), sc(74)], fill=brow_color)
    d.ellipse([sc(110), sc(64), sc(136), sc(72)], fill=head_color)

    # Nose
    nose_color = (60, 30, 20)
    nose_shine = (90, 50, 40)
    d.ellipse([sc(82), sc(108), sc(110), sc(128)], fill=nose_color)
    d.ellipse([sc(84), sc(110), sc(96), sc(118)], fill=nose_shine)
    # Nostrils
    d.ellipse([sc(84), sc(114), sc(92), sc(124)], fill=(30, 10, 5))
    d.ellipse([sc(100), sc(114), sc(108), sc(124)], fill=(30, 10, 5))

    # Mouth / smile
    mouth_color = (160, 80, 60)
    # Center line
    d.rectangle([sc(95), sc(128), sc(98), sc(138)], fill=mouth_color)
    # Smile curves
    for i in range(12):
        angle = math.pi + math.pi * i / 24
        rx, ry = sc(16), sc(10)
        x = sc(80) + int(rx * math.cos(angle))
        y = sc(138) + int(ry * math.sin(angle))
        d.ellipse([x-2, y-2, x+2, y+2], fill=mouth_color)
    for i in range(12):
        angle = math.pi * 2 - math.pi * i / 24
        rx, ry = sc(16), sc(10)
        x = sc(112) + int(rx * math.cos(angle))
        y = sc(138) + int(ry * math.sin(angle))
        d.ellipse([x-2, y-2, x+2, y+2], fill=mouth_color)

    # Tongue
    tongue_color = (220, 80, 100)
    tongue_dark = (190, 60, 80)
    d.ellipse([sc(84), sc(136), sc(108), sc(160)], fill=tongue_color)
    d.rectangle([sc(93), sc(148), sc(99), sc(160)], fill=tongue_dark)

    # Inner ear detail
    inner_ear = (190, 130, 90)
    d.ellipse([sc(40), sc(44), sc(70), sc(94)], fill=inner_ear)
    d.ellipse([sc(122), sc(44), sc(152), sc(94)], fill=inner_ear)

    # Cheek blush
    blush = (255, 160, 160, 80)
    d.ellipse([sc(38), sc(100), sc(68), sc(128)], fill=blush)
    d.ellipse([sc(124), sc(100), sc(154), sc(128)], fill=blush)

    # Small highlight on head
    d.ellipse([sc(70), sc(46), sc(100), sc(66)], fill=(240, 210, 170, 120))

    return img


sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

base = "/home/user/Barky1/res"
for folder, size in sizes.items():
    out_dir = os.path.join(base, folder)
    os.makedirs(out_dir, exist_ok=True)
    img = draw_dog_icon(size)
    path = os.path.join(out_dir, "ic_launcher.png")
    img.save(path, "PNG")
    print(f"  {path} ({size}x{size})")

# Also save foreground/background for adaptive icons
# and a large version for reference
img = draw_dog_icon(512)
img.save("/home/user/Barky1/res/drawable-xxxhdpi/ic_launcher.png", "PNG")
img.save("/home/user/Barky1/res/drawable-xxhdpi/ic_launcher.png", "PNG")
img.save("/home/user/Barky1/res/drawable-xhdpi/ic_launcher.png", "PNG")
img.save("/home/user/Barky1/res/drawable-hdpi/ic_launcher.png", "PNG")
img.save("/home/user/Barky1/res/drawable-mdpi/ic_launcher.png", "PNG")

print("Dog icon generated successfully!")
