.class public Lcom/barky/soundboard/MainActivity;
.super Landroid/app/Activity;
.implements Landroid/view/View$OnClickListener;
.implements Landroid/media/MediaPlayer$OnCompletionListener;

.field private mCurrentPlayer:Landroid/media/MediaPlayer;


# Constructor
.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method


# Set up layout and attach click listeners to all buttons
.method protected onCreate(Landroid/os/Bundle;)V
    .registers 4

    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    const v0, 0x7f040000
    invoke-virtual {p0, v0}, Landroid/app/Activity;->setContentView(I)V

    const v0, 0x7f090000
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_0
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_0

    const v0, 0x7f090001
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_1
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_1

    const v0, 0x7f090002
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_2
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_2

    const v0, 0x7f090003
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_3
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_3

    const v0, 0x7f090004
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_4
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_4

    const v0, 0x7f090005
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_5
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_5

    const v0, 0x7f090006
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_6
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_6

    const v0, 0x7f090007
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_7
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_7

    const v0, 0x7f090008
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_8
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_8

    const v0, 0x7f090009
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_9
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_9

    const v0, 0x7f09000a
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_10
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_10

    const v0, 0x7f09000b
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_11
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_11

    const v0, 0x7f09000c
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_12
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_12

    const v0, 0x7f09000d
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_13
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_13

    const v0, 0x7f09000e
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_14
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_14

    const v0, 0x7f09000f
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_15
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_15

    const v0, 0x7f090010
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_16
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_16

    const v0, 0x7f090011
    invoke-virtual {p0, v0}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v1
    if-eqz v1, :cond_17
    invoke-virtual {v1, p0}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    :cond_17

    return-void
.end method


# Handle button clicks - stop current sound and play new one
.method public onClick(Landroid/view/View;)V
    .registers 5
    # p0=this, p1=View, v0=MediaPlayer, v1=viewId, v2=soundResId

    iget-object v0, p0, Lcom/barky/soundboard/MainActivity;->mCurrentPlayer:Landroid/media/MediaPlayer;
    if-eqz v0, :cond_no_current
    invoke-virtual {v0}, Landroid/media/MediaPlayer;->release()V
    const/4 v0, 0x0
    iput-object v0, p0, Lcom/barky/soundboard/MainActivity;->mCurrentPlayer:Landroid/media/MediaPlayer;
    :cond_no_current

    invoke-virtual {p1}, Landroid/view/View;->getId()I
    move-result v1

    packed-switch v1, :pswitch_data

    return-void

    :pswitch_0
    const v2, 0x7f050003
    goto :play_sound

    :pswitch_1
    const v2, 0x7f050007
    goto :play_sound

    :pswitch_2
    const v2, 0x7f050008
    goto :play_sound

    :pswitch_3
    const v2, 0x7f05000d
    goto :play_sound

    :pswitch_4
    const v2, 0x7f050002
    goto :play_sound

    :pswitch_5
    const v2, 0x7f05000a
    goto :play_sound

    :pswitch_6
    const v2, 0x7f050000
    goto :play_sound

    :pswitch_7
    const v2, 0x7f050005
    goto :play_sound

    :pswitch_8
    const v2, 0x7f05000b
    goto :play_sound

    :pswitch_9
    const v2, 0x7f05000f
    goto :play_sound

    :pswitch_10
    const v2, 0x7f05000c
    goto :play_sound

    :pswitch_11
    const v2, 0x7f050006
    goto :play_sound

    :pswitch_12
    const v2, 0x7f050004
    goto :play_sound

    :pswitch_13
    const v2, 0x7f050010
    goto :play_sound

    :pswitch_14
    const v2, 0x7f050001
    goto :play_sound

    :pswitch_15
    const v2, 0x7f050009
    goto :play_sound

    :pswitch_16
    const v2, 0x7f05000e
    goto :play_sound

    :pswitch_17
    const v2, 0x7f050011
    goto :play_sound

    :play_sound
    invoke-static {p0, v2}, Landroid/media/MediaPlayer;->create(Landroid/content/Context;I)Landroid/media/MediaPlayer;
    move-result-object v0
    if-eqz v0, :cond_null_mp
    iput-object v0, p0, Lcom/barky/soundboard/MainActivity;->mCurrentPlayer:Landroid/media/MediaPlayer;
    invoke-virtual {v0, p0}, Landroid/media/MediaPlayer;->setOnCompletionListener(Landroid/media/MediaPlayer$OnCompletionListener;)V
    invoke-virtual {v0}, Landroid/media/MediaPlayer;->start()V
    :cond_null_mp
    return-void

    :pswitch_data
    .packed-switch 0x7f090000
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
        :pswitch_5
        :pswitch_6
        :pswitch_7
        :pswitch_8
        :pswitch_9
        :pswitch_10
        :pswitch_11
        :pswitch_12
        :pswitch_13
        :pswitch_14
        :pswitch_15
        :pswitch_16
        :pswitch_17
    .end packed-switch

.end method


# Release MediaPlayer when sound finishes
.method public onCompletion(Landroid/media/MediaPlayer;)V
    .registers 3
    invoke-virtual {p1}, Landroid/media/MediaPlayer;->release()V
    const/4 v0, 0x0
    iput-object v0, p0, Lcom/barky/soundboard/MainActivity;->mCurrentPlayer:Landroid/media/MediaPlayer;
    return-void
.end method


# Release MediaPlayer when activity is destroyed
.method protected onDestroy()V
    .registers 2
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V
    iget-object v0, p0, Lcom/barky/soundboard/MainActivity;->mCurrentPlayer:Landroid/media/MediaPlayer;
    if-eqz v0, :cond_done
    invoke-virtual {v0}, Landroid/media/MediaPlayer;->release()V
    :cond_done
    return-void
.end method
