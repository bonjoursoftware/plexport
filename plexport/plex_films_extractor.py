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
import os
import requests
import urllib3

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class PlexFilmsExtractor:
    host: str
    port: int = 32400

    def extract_plex_films(self) -> Dict[Any, Any]:
        page_offset = 0
        page_size = 100
        token = os.getenv("PLEX_API_TOKEN") or input("Plex API token: ")
        plex_films = self._extract_films_page(token, page_offset, page_size)
        while self._has_more_films(plex_films, page_offset, page_size):
            page_offset += page_size
            plex_films["MediaContainer"]["Metadata"].extend(
                self._extract_films_page(token, page_offset, page_size)["MediaContainer"]["Metadata"]
            )
        return plex_films

    def _extract_films_page(self, plex_token: str, page_offset: int, page_size: int) -> Dict[Any, Any]:
        url = (
            f"https://{self.host}:{self.port}/library/sections/1/all?type=1&includeCollections=1"
            f"&includeAdvanced=1&includeMeta=1&X-Plex-Container-Start={page_offset}"
            f"&X-Plex-Container-Size={page_size}"
            f"&X-Plex-Token={plex_token}"
        )
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en-GB",
        }
        return dict(requests.get(url, headers=headers, verify=False).json())

    @staticmethod
    def _has_more_films(plex_db: Dict[Any, Any], page_offset: int, page_size: int) -> bool:
        return int(plex_db["MediaContainer"]["totalSize"]) > (page_offset / page_size + 1) * page_size


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
