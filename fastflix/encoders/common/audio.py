#!/usr/bin/env python
# -*- coding: utf-8 -*-

channel_list = {
    "mono": 1,
    "stereo": 2,
    "2.1": 3,
    "3.0": 3,
    "3.0(back)": 3,
    "3.1": 4,
    "4.0": 4,
    "quad": 4,
    "quad(side)": 4,
    "5.0": 5,
    "5.1": 6,
    "6.0": 6,
    "6.0(front)": 6,
    "hexagonal": 6,
    "6.1": 7,
    "6.1(front)": 7,
    "7.0": 7,
    "7.0(front)": 7,
    "7.1": 8,
    "7.1(wide)": 8,
}

reverse_channel_lookup = {1: "mono", 2: "stereo", 3: "2.1", 4: "3.1", 5: "5.0", 6: "5.1", 7: "6.1", 8: "7.1"}

lossless = ["flac", "truehd", "alac", "tta", "wavpack", "mlp"]


def build_audio(audio_tracks, audio_file_index=0):
    command_list = []
    for track in audio_tracks:
        command_list.append(
            f"-map {audio_file_index}:{track.index} "
            f'-metadata:s:{track.outdex} title="{track.title}" '
            f'-metadata:s:{track.outdex} handler="{track.title}"'
        )
        if track.downmix:
            channel_layout = track.downmix
        else:
            try:
                channel_layout = track.channel_layout or reverse_channel_lookup[track.channels]
            except KeyError:
                raise Exception(f"Cannot determine audio layout for track {track.index}")

        if track.filter_text:
            audio_filter = f"aformat=channel_layouts={channel_layout}:{track.filter_text}"
        else:
            audio_filter = f"aformat=channel_layouts={channel_layout}"
        command_list.append(f" -filter:{track.outdex} {audio_filter}")

        if track.language:
            command_list.append(f"-metadata:s:{track.outdex} language={track.language}")
        if not track.conversion_codec or track.conversion_codec == "none":
            command_list.append(f"-c:{track.outdex} copy")
        elif track.conversion_codec:
            downmix = f"-ac:{track.outdex} {channel_list[track.downmix]}" if track.downmix else ""
            bitrate = ""
            if track.conversion_codec not in lossless:
                bitrate = f"-b:{track.outdex} {track.conversion_bitrate} "
            command_list.append(f"-c:{track.outdex} {track.conversion_codec} {bitrate} {downmix}")

    return " ".join(command_list)
