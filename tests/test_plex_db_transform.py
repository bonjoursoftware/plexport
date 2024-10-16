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
import json

from plexport.plex_db_transform import transform_plex_db


def test_transform_plex_db() -> None:
    with open("./tests/resources/test_plex_db_export.json", "r") as plex_db_export_file:
        plex_db_export = json.load(plex_db_export_file)
    assert transform_plex_db(plex_db_export) == [
        {
            "name": "Big Buck Bunny (2008) (Sacha Goedegebure) " "(Blender Foundation 2008, Janus Bager Kristensen 2013) (Animation)",
            "notes": "0h10m34s - 3.5Mbps h264 high - 6ch ac3 - 276.1MB /movies/bbb_sunflower_1080p_30fps_normal.mp4",
            "tags": ["all", "1080", "unwatched"],
            "ref": "https://www.themoviedb.org/movie/10378/",
        },
        {
            "name": "2020-11-14 - Big Buck Bunny (2008) (Sacha Goedegebure) (Blender Foundation 2008, Janus Bager Kristensen 2013) (Animation)",
            "notes": "0h10m34s - 3.5Mbps h264 high - 6ch ac3 - 276.1MB /movies/bbb_sunflower_1080p_30fps_normal.mp4",
            "tags": ["_added_dates"],
            "ref": "https://www.themoviedb.org/movie/10378/",
        },
        {
            "name": "Elephants Dream (2006) (Bassam Kurdali) (Tygo Gernandt, Cas Jansen) (Animation, Science Fiction)",
            "notes": "0h10m53s - 0.8Mbps h264 constrained baseline - 2ch aac lc - 67.8MB /movies/ed_hd.mp4",
            "tags": ["all", "sd", "watched"],
            "ref": "https://www.imdb.com/title/tt0807840/",
        },
        {
            "name": "2014-11-03 - Elephants Dream (2006) (Bassam Kurdali) (Tygo Gernandt, Cas Jansen) (Animation, Science Fiction)",
            "notes": "0h10m53s - 0.8Mbps h264 constrained baseline - 2ch aac lc - 67.8MB /movies/ed_hd.mp4",
            "tags": ["_added_dates"],
            "ref": "https://www.imdb.com/title/tt0807840/",
        },
        {
            "name": "2021-04-10 - Elephants Dream (2006) (Bassam Kurdali) (Tygo Gernandt, Cas Jansen) (Animation, Science Fiction)",
            "notes": "0h10m53s - 0.8Mbps h264 constrained baseline - 2ch aac lc - 67.8MB /movies/ed_hd.mp4",
            "tags": ["_watched_dates"],
            "ref": "https://www.imdb.com/title/tt0807840/",
        },
        {
            "name": "A fantastic test film (2999) (Joe) (Bob, Ken) (unspecified)",
            "notes": "0h02m03s - 2.0Mbps h999 constrained baseline - 2ch cod pro - 88.6MB /movies/fantastic.mp4",
            "tags": ["all", "hd", "unwatched", "dupe"],
            "ref": "https://www.imdb.com/search/title/?title=A%20fantastic%20test%20film&release_date=2999-01-01,",
        },
        {
            "name": "2014-11-03 - A fantastic test film (2999) (Joe) (Bob, Ken) (unspecified)",
            "notes": "0h02m03s - 2.0Mbps h999 constrained baseline - 2ch cod pro - 88.6MB /movies/fantastic.mp4",
            "tags": ["_added_dates"],
            "ref": "https://www.imdb.com/search/title/?title=A%20fantastic%20test%20film&release_date=2999-01-01,",
        },
        {
            "name": "A film with no year (year unknown) (Joe) (Bob, Ken) (unspecified)",
            "notes": "0h02m03s - 2.0Mbps h999 constrained baseline - 2ch cod pro - 88.6MB /movies/fantastic.mp4",
            "tags": ["all", "hd", "unwatched", "dupe"],
            "ref": "https://www.imdb.com/search/title/?title=A%20film%20with%20no%20year",
        },
        {
            "name": "2014-10-28 - A film with no year (year unknown) (Joe) (Bob, Ken) (unspecified)",
            "notes": "0h02m03s - 2.0Mbps h999 constrained baseline - 2ch cod pro - 88.6MB /movies/fantastic.mp4",
            "tags": ["_added_dates"],
            "ref": "https://www.imdb.com/search/title/?title=A%20film%20with%20no%20year",
        },
    ]
