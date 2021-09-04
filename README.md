# Plexport

[Bonjour Software][bonjoursoftware] [Plexport][plexport] is a command-line tool that can perform ETL operations against
a Plex Media Server instance.

## Features

- extract film collections from a Plex Media Server
- transform extracted data into a json schema understood by [MyCollections][mycollections]

## Development roadmap

- add a load step that can import extracted data into a MondoDB instance for [MyCollections][mycollections] 
- expand extraction capability to series
- add transformation of extracted series into a json schema understood by [MyCollections][mycollections]

[bonjoursoftware]: https://bonjour.software
[plexport]: https://github.com/bonjoursoftware/plexport
[mycollections]: https://github.com/bonjoursoftware/mycollections
