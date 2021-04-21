#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import secrets

import reusables

from fastflix.encoders.common.helpers import Command, generate_filters, generate_color_details, null
from fastflix.models.encode import VVenCSettings
from fastflix.models.fastflix import FastFlix

logger = logging.getLogger("fastflix")


@reusables.log_exception("fastflix", show_traceback=True)
def build(fastflix: FastFlix):
    settings: VVenCSettings = fastflix.current_video.video_settings.video_encoder_settings

    # ffmpeg -t 0.5 -i ducks.mp4 -pix_fmt yuv420p10le -an -dn -sn -r 30 -f yuv4mpegpipe -strict -1 - | ./vvencapp -s 1920x1080 -r 30 -i - -c yuv420_10 -o ducks_pipe.vvc
    # ffmpeg -i ducks.mp4 -pix_fmt yuv420p10le -an -dn -sn -r 30 -f rawvideo -strict -1 - | ./vvenc_linux/vvencapp -s 1920x1080 -r 30 -i - -c yuv420_10 -o ducks_pipe.vvc --preset faster

    command = [
        "ffmpeg",
        "-i",
        fastflix.current_video.source,
        " -pix_fmt yuv420p10le -an -dn -sn -r 30 -f yuv4mpegpipe -strict -1 -",
        generate_filters(source=fastflix.current_video.source, **fastflix.current_video.video_settings.dict()),
    ]

    options = {
        "InputFile": "-",
        "InputBitDepth": fastflix.current_video.current_video_stream.bit_depth,
        "FrameRate": fastflix.current_video.frame_rate,
        "SourceWidth": fastflix.current_video.width,
        "SourceHeight": fastflix.current_video.height,
        "Verbosity": 6,
        "OutputBitDepth": 10,
        "BitstreamFile": str(fastflix.current_video.video_settings.output_path),
        "preset": settings.preset,
        "Tier": settings.tier,
        "PerceptQPA": int(settings.qpa),
        "Threads": 8,  # do cpu count?
    }

    if settings.bitrate:
        options["TargetBitrate"] = settings.bitrate
    else:
        options["QP"] = settings.qp

    if settings.pix_fmt in ("yuv420p10le", "yuv420p12le"):

        if fastflix.current_video.master_display:
            options["Hdr"] = "hdr10_2020"
            options["MasteringDisplayColourVolume"] = (
                f"{fastflix.current_video.master_display.green}{fastflix.current_video.master_display.blue}{fastflix.current_video.master_display.red}{fastflix.current_video.master_display.white}{fastflix.current_video.master_display.luminance}".replace(
                    ")", ","
                )
                .replace("(", "")
                .strip(",")
            )

        if fastflix.current_video.cll:
            options["MaxContentLightLevel"] = fastflix.current_video.cll.strip("()")

    from pprint import pprint

    pprint(options)

    with open(fastflix.current_video.work_path / "options.cfg", "w") as f:

        f.writelines([f"{k}: {v}\n" for k, v in options.items()])

    return [
        Command(
            command=f"ffmpeg -i {fastflix.current_video.source} "
            f"-map 0:{fastflix.current_video.current_video_stream.index}"
            f"-f rawvideo - | vvencFFapp -c \"{fastflix.current_video.work_path / 'options.cfg'}\" ",
            name=f"VVC Encode",
            exe="ffmpeg",
        ),
    ]

    # beginning, ending = generate_all(fastflix, "libsvtav1")

    # beginning += f"-strict experimental "
    #
    # if not settings.single_pass:
    #     pass_log_file = fastflix.current_video.work_path / f"pass_log_file_{secrets.token_hex(10)}"
    #     beginning += f'-passlogfile "{pass_log_file}" '
    #
    # pass_type = "bitrate" if settings.bitrate else "QP"
    #
    # if settings.single_pass:
    #     if settings.bitrate:
    #         command_1 = f"{beginning} -b:v {settings.bitrate} -rc 1 {settings.extra} {ending}"
    #
    #     elif settings.qp is not None:
    #         command_1 = f"{beginning} -qp {settings.qp} -rc 0 {settings.extra} {ending}"
    #     else:
    #         return []
    #     return [Command(command=command_1, name=f"{pass_type}", exe="ffmpeg")]
    # else:
    #     if settings.bitrate:
    #         command_1 = f"{beginning} -b:v {settings.bitrate} -rc 1 -pass 1 {settings.extra if settings.extra_both_passes else ''} -an -f matroska {null}"
    #         command_2 = f"{beginning} -b:v {settings.bitrate} -rc 1 -pass 2 {settings.extra} {ending}"
    #
    #     elif settings.qp is not None:
    #         command_1 = f"{beginning} -qp {settings.qp} -rc 0 -pass 1 {settings.extra if settings.extra_both_passes else ''} -an -f matroska {null}"
    #         command_2 = f"{beginning} -qp {settings.qp} -rc 0 -pass 2 {settings.extra} {ending}"
    #     else:
    #         return []
    #     return [
    #         Command(command=command_1, name=f"First pass {pass_type}", exe="ffmpeg"),
    #         Command(command=command_2, name=f"Second pass {pass_type} ", exe="ffmpeg"),
    #     ]
