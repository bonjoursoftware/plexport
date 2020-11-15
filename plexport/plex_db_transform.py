# Plexport - Plex Media Server database ETL
#
# https://github.com/bonjoursoftware/plexport
#
# Copyright (C) 2020 Bonjour Software Limited
#
# https://bonjoursoftware.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see
# https://github.com/bonjoursoftware/plexport/blob/master/LICENSE
import logging
import re

from typing import Any, Dict, List


def transform_plex_db(plex_db_export: Dict[Any, Any]) -> List[Dict[str, str]]:
    return [_transform(film) for film in plex_db_export["MediaContainer"]["Metadata"]]


def _transform(film: Dict[Any, Any]) -> Dict[str, str]:
    try:
        return {
            "name": _build_title(film),
            "notes": _build_notes(film),
            "tags": _build_tags(film),
            "ref": _build_ref(film),
        }
    except Exception as error:
        logging.warning(f"unable to process film [{film['title']}]: {error}")


def _build_title(film: Dict[Any, Any]) -> str:
    return f"{film.get('title')} ({film.get('year')})"


def _build_notes(film: Dict[Any, Any]) -> str:
    media = film.get("Media")[0]
    part = media.get("Part")[0]
    return (
        f"{_build_duration(film)} - "
        f"{_build_bitrate(film)} {media.get('videoCodec')} {media.get('videoProfile')} - "
        f"{media.get('audioChannels')}ch {media.get('audioCodec')} {_build_audio_profile(part.get('audioProfile'))}- "
        f"{_build_size(part.get('size'))} {part.get('file')}"
    )


def _build_duration(film: Dict[Any, Any]) -> str:
    duration = film.get("Media")[0].get("duration")
    h = duration // 3_600_000
    m = duration % 3_600_000 // 60_000
    s = duration % 3_600_000 % 60_000 / 1_000
    return "%dh%02dm%02ds" % (h, m, s)


def _build_bitrate(film: Dict[Any, Any]) -> str:
    return "%.1fMbps" % (film.get("Media")[0].get("bitrate") / 1_000,)


def _build_audio_profile(audio_profile: str) -> str:
    return f"{audio_profile} " if audio_profile else ""


def _build_size(size: int) -> str:
    return "%.1fMB" % (size / 1_000_000,)


def _build_tags(film: Dict[Any, Any]) -> List[str]:
    return ["all", film.get("Media")[0].get("videoResolution")]


def _build_imdb_ref(guid: str) -> str:
    imdb_id = re.search("tt\\d+", guid).group()
    return f"https://www.imdb.com/title/{imdb_id}/"


def _build_themoviedb_ref(guid: str) -> str:
    themoviedb_id = re.search("\\d+", guid).group()
    return f"https://www.themoviedb.org/movie/{themoviedb_id}/"


def _build_unsupported_ref(guid: str) -> str:
    logging.warning(f"unsupported guid: {guid}")
    return ""


_agents_ref_map = {
    "com.plexapp.agents.imdb": _build_imdb_ref,
    "com.plexapp.agents.themoviedb": _build_themoviedb_ref,
}


def _build_ref(film: Dict[Any, Any]) -> str:
    guid = film.get("guid")
    agent = re.search("^\\S+(?=:)", guid).group()
    return _agents_ref_map.get(agent, _build_unsupported_ref)(guid)
