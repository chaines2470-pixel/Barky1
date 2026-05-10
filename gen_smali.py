#!/usr/bin/env python3
"""Generate MainActivity.smali for Barky soundboard app."""
import os

BUTTONS = [
    (0x7f090000, 0x7f050003, "chihuahua"),
    (0x7f090001, 0x7f050007, "german_shepherd"),
    (0x7f090002, 0x7f050008, "golden_retriever"),
    (0x7f090003, 0x7f05000d, "poodle"),
    (0x7f090004, 0x7f050002, "bulldog"),
    (0x7f090005, 0x7f05000a, "husky"),
    (0x7f090006, 0x7f050000, "beagle"),
    (0x7f090007, 0x7f050005, "dachshund"),
    (0x7f090008, 0x7f05000b, "labrador"),
    (0x7f090009, 0x7f05000f, "rottweiler"),
    (0x7f09000a, 0x7f05000c, "pomeranian"),
    (0x7f09000b, 0x7f050006, "doberman"),
    (0x7f09000c, 0x7f050004, "corgi"),
    (0x7f09000d, 0x7f050010, "shihtzu"),
    (0x7f09000e, 0x7f050001, "border_collie"),
    (0x7f09000f, 0x7f050009, "great_dane"),
    (0x7f090010, 0x7f05000e, "puppy"),
    (0x7f090011, 0x7f050011, "wolf"),
]

LAYOUT_ID = 0x7f040000
FIELD = "Lcom/barky/soundboard/MainActivity;->mCurrentPlayer:Landroid/media/MediaPlayer;"

lines = []
def L(s=""): lines.append(s)

L(".class public Lcom/barky/soundboard/MainActivity;")
L(".super Landroid/app/Activity;")
L(".implements Landroid/view/View$OnClickListener;")
L(".implements Landroid/media/MediaPlayer$OnCompletionListener;")
L()
L(".field private mCurrentPlayer:Landroid/media/MediaPlayer;")
L()
L()
L("# Constructor")
L(".method public constructor <init>()V")
L("    .registers 1")
L("    invoke-direct {p0}, Landroid/app/Activity;-><init>()V")
L("    return-void")
L(".end method")
L()
L()
L("# Set up layout and attach click listeners to all buttons")
L(".method protected onCreate(Landroid/os/Bundle;)V")
L("    .registers 4")
L()
L("    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V")
L()
L(f"    const v0, {hex(LAYOUT_ID)}")
L("    invoke-virtual {p0, v0}, Landroid/app/Activity;->setContentView(I)V")
L()

for i, (btn_id, sound_id, name) in enumerate(BUTTONS):
    L(f"    const v0, {hex(btn_id)}")
    L("    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;")
    L("    move-result-object v1")
    L(f"    if-eqz v1, :cond_{i}")
    L("    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V")
    L(f"    :cond_{i}")
    L()

L("    return-void")
L(".end method")
L()
L()
L("# Handle button clicks - stop current sound and play new one")
L(".method public onClick(Landroid/view/View;)V")
L("    .registers 5")
L("    # p0=this, p1=View, v0=MediaPlayer, v1=viewId, v2=soundResId")
L()
L(f"    iget-object v0, p0, {FIELD}")
L("    if-eqz v0, :cond_no_current")
L("    invoke-virtual {v0}, Landroid/media/MediaPlayer;->release()V")
L("    const/4 v0, 0x0")
L(f"    iput-object v0, p0, {FIELD}")
L("    :cond_no_current")
L()
L("    invoke-virtual {p1}, Landroid/view/View;->getId()I")
L("    move-result v1")
L()
L("    packed-switch v1, :pswitch_data")
L()
L("    return-void")
L()

for i, (btn_id, sound_id, name) in enumerate(BUTTONS):
    L(f"    :pswitch_{i}")
    L(f"    const v2, {hex(sound_id)}")
    L("    goto :play_sound")
    L()

L("    :play_sound")
L("    invoke-static {p0, v2}, Landroid/media/MediaPlayer;->create(Landroid/content/Context;I)Landroid/media/MediaPlayer;")
L("    move-result-object v0")
L("    if-eqz v0, :cond_null_mp")
L(f"    iput-object v0, p0, {FIELD}")
L("    invoke-virtual {v0, p0}, Landroid/media/MediaPlayer;->setOnCompletionListener(Landroid/media/MediaPlayer$OnCompletionListener;)V")
L("    invoke-virtual {v0}, Landroid/media/MediaPlayer;->start()V")
L("    :cond_null_mp")
L("    return-void")
L()
L(f"    :pswitch_data")
L(f"    .packed-switch {hex(BUTTONS[0][0])}")
for i in range(len(BUTTONS)):
    L(f"        :pswitch_{i}")
L("    .end packed-switch")
L()
L(".end method")
L()
L()
L("# Release MediaPlayer when sound finishes")
L(".method public onCompletion(Landroid/media/MediaPlayer;)V")
L("    .registers 3")
L("    invoke-virtual {p1}, Landroid/media/MediaPlayer;->release()V")
L("    const/4 v0, 0x0")
L(f"    iput-object v0, p0, {FIELD}")
L("    return-void")
L(".end method")
L()
L()
L("# Release MediaPlayer when activity is destroyed")
L(".method protected onDestroy()V")
L("    .registers 2")
L("    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V")
L(f"    iget-object v0, p0, {FIELD}")
L("    if-eqz v0, :cond_done")
L("    invoke-virtual {v0}, Landroid/media/MediaPlayer;->release()V")
L("    :cond_done")
L("    return-void")
L(".end method")

out = "\n".join(lines) + "\n"
out_path = "/home/user/Barky1/src/com/barky/soundboard/MainActivity.smali"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    f.write(out)
print(f"Written: {out_path} ({len(lines)} lines)")
