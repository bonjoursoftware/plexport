# Plexport - Plex Media Server database ETL
#
# https://github.com/bonjoursoftware/plexport
#
# Copyright (C) 2020 - 2021 Bonjour Software Limited
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
import json

from typing import Any, Dict
from unittest.mock import patch, Mock

from plexport.plex_films_extractor import PlexFilmsExtractor


def _load_json_file(index: int) -> Dict[str, Any]:
    with open(f"./tests/resources/test_plex_films_export_page_0{index}.json", "r") as json_file:
        return dict(json.load(json_file))


def test_plex_films_extractor(monkeypatch: Any) -> None:
    mock_get = Mock(
        side_effect=[
            Mock(json=Mock(return_value=_load_json_file(1))),
            Mock(json=Mock(return_value=_load_json_file(2))),
            Mock(json=Mock(return_value=_load_json_file(3))),
        ]
    )
    monkeypatch.setenv("PLEX_API_TOKEN", "super_secret")

    with patch("requests.get", mock_get):
        plex_films = PlexFilmsExtractor(host="localhost").extract_plex_films()

    mock_get.assert_called_with(
        (
            "https://localhost:32400/library/sections/1/all?type=1&includeCollections=1&includeAdvanced=1&includeMeta=1"
            "&X-Plex-Container-Start=200&X-Plex-Container-Size=100&X-Plex-Token=super_secret"
        ),
        headers={"Accept": "application/json", "Accept-Language": "en-GB"},
        verify=False,
    )

    for index in range(0, 224):
        assert plex_films["MediaContainer"]["Metadata"][index]["title"] == "Film %03d" % (index + 1,)
