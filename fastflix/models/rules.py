#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import List, Optional, Union, Dict

from pydantic import BaseModel, Field
from box import Box


class AudioSelectRule(BaseModel):
    action_type: str
    selected_action: str
    match_type: str
    selected_match: List[str]


class AudioSortRule(BaseModel):
    sort_type: str
    selected_sort_option: str
