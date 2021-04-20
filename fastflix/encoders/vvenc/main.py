#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Chris Griffith"
from pathlib import Path

import pkg_resources

name = "VVC (VVenC)"

video_extension = ".vvc"
video_dimension_divisor = 8
icon = str(Path(pkg_resources.resource_filename(__name__, f"../../data/encoders/icon_vvc.png")).resolve())

enable_subtitles = False
enable_audio = False
enable_attachments = False

audio_formats = []

from fastflix.encoders.vvenc.command_builder import build
from fastflix.encoders.vvenc.settings_panel import VVenC as settings_panel
