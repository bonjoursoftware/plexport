# Plexport - Plex Media Server database ETL
#
# https://github.com/bonjoursoftware/plexport
#
# Copyright (C) 2020 - 2023 Bonjour Software Limited
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
#
import logging
import re

from datetime import datetime
from itertools import chain
from requests.utils import requote_uri
from typing import Any, Dict, List, Optional, Union


def transform_plex_db(plex_db_export: Dict[str, Any]) -> List[Dict[str, Union[str, List[str]]]]:
    return list(chain.from_iterable(filter(None, [_transform(film) for film in plex_db_export["MediaContainer"]["Metadata"]])))


def _transform(film: Dict[str, Any]) -> Optional[List[Dict[str, Union[str, List[str]]]]]:
    try:
        title, notes, ref = _build_title(film), _build_notes(film), _build_ref(film)
        return list(
            filter(
                None,
                [
                    {"name": title, "notes": notes, "tags": _build_tags(film), "ref": ref},
                    {"name": _with_added_date(title, film), "notes": notes, "tags": ["_added_dates"], "ref": ref},
                    {"name": _with_watched_date(title, film), "notes": notes, "tags": ["_watched_dates"], "ref": ref} if film.get("lastViewedAt") else None,
                ],
            )
        )
    except Exception as error:
        logging.warning(f"unable to process film [{film}]: {error}")
        return None


def _build_title(film: Dict[Any, Any]) -> str:
    return (
        f"{film.get('title')} "
        f"({film.get('year', 'year unknown')}) "
        f"({_build_tag_enum(film.get('Director'))}) "
        f"({_build_tag_enum(film.get('Role'))}) "
        f"({_build_tag_enum(film.get('Genre'))})"
    )


def _with_added_date(title: str, film: Dict[Any, Any]) -> str:
    return f"{datetime.fromtimestamp(film['addedAt']).strftime('%Y-%m-%d')} - {title}"


def _with_watched_date(title: str, film: Dict[Any, Any]) -> str:
    return f"{datetime.fromtimestamp(film['lastViewedAt']).strftime('%Y-%m-%d')} - {title}"


def _build_tag_enum(items: Optional[List[Dict[str, str]]]) -> str:
    return ", ".join([item["tag"] for item in items]) if items else "unspecified"


def _build_notes(film: Dict[Any, Any]) -> str:
    media = film["Media"][0]
    part = media["Part"][0]
    return (
        f"{_build_duration(film)} - "
        f"{_build_bitrate(film)} {media.get('videoCodec')} {media.get('videoProfile')} - "
        f"{media.get('audioChannels')}ch {media.get('audioCodec')} {_build_audio_profile(part.get('audioProfile'))}- "
        f"{_build_size(part.get('size'))} {part.get('file')}"
    )


def _build_duration(film: Dict[Any, Any]) -> str:
    duration = film["Media"][0]["duration"]
    h = duration // 3_600_000
    m = duration % 3_600_000 // 60_000
    s = duration % 3_600_000 % 60_000 / 1_000
    return "%dh%02dm%02ds" % (h, m, s)


def _build_bitrate(film: Dict[Any, Any]) -> str:
    return "%.1fMbps" % (film["Media"][0]["bitrate"] / 1_000,)


def _build_audio_profile(audio_profile: str) -> str:
    return f"{audio_profile} " if audio_profile else ""


def _build_size(size: int) -> str:
    return "%.1fMB" % (size / 1_000_000,)


def _build_tags(film: Dict[Any, Any]) -> List[str]:
    return [
        "all",
        f"{film['Media'][0]['videoResolution']}",
        "watched" if film.get("lastViewedAt") else "unwatched",
    ] + (["dupe"] if len(film["Media"]) > 1 else [])


def _build_imdb_ref(guid: str, title: str, year: int) -> str:
    match = re.search("tt\\d+", guid)
    imdbid = match.group() if match else None
    return f"https://www.imdb.com/title/{imdbid}/" if imdbid else _build_unsupported_ref(guid, title, year)


def _build_themoviedb_ref(guid: str, title: str, year: int) -> str:
    match = re.search("\\d+", guid)
    themoviedbid = match.group() if match else None
    return f"https://www.themoviedb.org/movie/{themoviedbid}/" if themoviedbid else _build_unsupported_ref(guid, title, year)


def _build_unsupported_ref(guid: str, title: str, year: int) -> str:
    # alternative: https://www.themoviedb.org/search/movie?query=some%20filme%20title
    return (
        f"https://www.imdb.com/search/title/?title={requote_uri(title)}&release_date={year}-01-01,"
        if year
        else f"https://www.imdb.com/search/title/?title={requote_uri(title)}"
    )


_agents_ref_map = {
    "com.plexapp.agents.imdb": _build_imdb_ref,
    "com.plexapp.agents.themoviedb": _build_themoviedb_ref,
}


def _build_ref(film: Dict[Any, Any]) -> str:
    guid, title, year = film["guid"], film["title"], film.get("year", 0)
    match = re.search("^\\S+(?=:)", guid)
    agent = match.group() if match else ""
    return _agents_ref_map.get(agent, _build_unsupported_ref)(guid, title, year)
