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
from plexport.plex_films_mycollections_importer import PlexFilmsMyCollectionsImporter

from mongita import MongitaClientMemory


def test_import_plex_films() -> None:
    films = [{"name": "film 1"}, {"name": "film 2"}]
    mongo_database = "test_db"
    mongo_collection = "test_col"
    mongo_client = MongitaClientMemory()

    PlexFilmsMyCollectionsImporter(mongo_client, mongo_database, mongo_collection).import_plex_films(films)

    col = mongo_client[mongo_database][mongo_collection]
    assert col.count_documents({}) == 2
    assert col.find_one({"name": "film 1"})
    assert col.find_one({"name": "film 2"})
