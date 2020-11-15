# [Bonjour Software Limited](https://bonjoursoftware.com/)

## Plexport

Bonjour Software's Plexport is a command-line tool that can perform ETL operations against a Plex Media Server instance.

## Features

* extract film collections from a Plex Media Server
* transform extracted data into a json schema understood by [MyCollections](https://github.com/bonjoursoftware/mycollections)

## Development roadmap:

* add a load step that can import extracted data into a [MyCollections](https://github.com/bonjoursoftware/mycollections) MondoDB instance
* expand extraction capability to series
* add transformation of extracted series into a json schema understood by [MyCollections](https://github.com/bonjoursoftware/mycollections)

## Technology stack

- Python 3
- Pytest
- Pipenv
- Docker
