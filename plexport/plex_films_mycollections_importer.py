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
from dataclasses import dataclass
from typing import Dict, List, Union

from pymongo import MongoClient


@dataclass
class PlexFilmsMyCollectionsImporter:
    mongo_client: MongoClient  # type: ignore[type-arg]
    mongo_database: str
    mongo_collection: str

    def import_plex_films(self, films: List[Dict[str, Union[str, List[str]]]]) -> None:
        collection = self.mongo_client[self.mongo_database][self.mongo_collection]
        collection.delete_many({})
        collection.insert_many(films)
