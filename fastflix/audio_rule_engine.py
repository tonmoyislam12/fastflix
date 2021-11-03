# -*- coding: utf-8 -*-
from typing import List, Union
from copy import deepcopy

from fastflix.models.encode import AudioTrack
from fastflix.models.rules import AudioSortRule, AudioSelectRule


sort_options = {"title": str, "track_id": int, "codec": str}


def run_rule_engine(audio_tracks: List[AudioTrack], task_list: List[Union[AudioSelectRule, AudioSortRule]]):
    audio_tracks = deepcopy(audio_tracks)
    for task in task_list:
        if isinstance(task, AudioSelectRule):
            audio_tracks = select_task(task, audio_tracks)
        elif isinstance(task, AudioSortRule):
            audio_tracks = sort_task(task, audio_tracks)
    return audio_tracks


def select_task(task: AudioSelectRule, audio: List[AudioTrack]):
    if task.selected_action == "all":
        return audio
    elif task.selected_action == "first":
        return audio[0]
    elif task.selected_action == "last":
        return audio[-1]

    if task.match_type == "equals":
        return list(filter(lambda x: getattr(x, task.selected_action) == task.selected_match[0], audio))
    if task.match_type == "contains":
        return list(filter(lambda x: str(getattr(x, task.selected_action)) == str(task.selected_match[0]), audio))
    if task.match_type == "one_of":
        return list(filter(lambda x: getattr(x, task.selected_action) in task.selected_match[0], audio))
    if task.match_type == "starts_with":
        return list(
            filter(lambda x: str(getattr(x, task.selected_action)).startswith(str(task.selected_match[0])), audio)
        )
    if task.match_type == "ends_with":
        return list(
            filter(lambda x: str(getattr(x, task.selected_action)).endswith(str(task.selected_match[0])), audio)
        )
    if task.match_type == "less_than":
        return list(filter(lambda x: getattr(x, task.selected_action) < task.selected_match[0], audio))
    if task.match_type == "greater_than":
        return list(filter(lambda x: getattr(x, task.selected_action) > task.selected_match[0], audio))


def sort_task(task: AudioSortRule, audio: List[AudioTrack]):
    pass
