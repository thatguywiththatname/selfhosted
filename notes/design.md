# notes-server Design

This is the intial design, not the final design

Variables in these notes are surrounded by {curly braces}

## Backend - Note Storage

All the notes are to be stored in a git repo with this structure:

`{repo-name}/year_{year_num}/notes/{unit_name}/{session_num}.md`

For example, this would be the path for the notes from the 3rd session of the WebF1 unit in 1st year:

`uni-repo/year_1/notes/webf1/3.md`

This Git repo will be periodically checked and notes-server will pull the repo when it changes

- All notes must be named only numbers
  - No duplicates
  - No leading 0's
- One note for each session
  - A session is one lecture, one practucal, etc.
- The first line in all notes must be a md title
  - `# this is a title`

## Frontend - Note Index

This is the HTML UI that will allow users to navigate the notes (like an index for a PFD or a Word doc)

The index is created like this:

- Years - The names of all the directories in `{repo-name}/`

Inside each years page:

- Units - The names of all the directories in `{repo-name}/year_{year_num}/notes/`

Inside each units page:

- Note Titles - The first line from each `.md` file in `{repo-name}/year_{year_num}/notes/{unit_name}/`, excluding the `#` and a space

## Frontend / Backend - Note URLs

Designed to be run under a `notes` sub-domain

E.g. `notes.example.com/year_1/webf1/3.html` will take you to the notes from the 3rd session of the webf1 unit from the 1st year

## Backend - Server Structure

The server is a Python 3 Flask web app

The code is formatted using Black

It is run using uWSGI and served using NGINX as a reverse proxy

See [uWSGI docs](https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html) about using it with NGINX

It uses [mistune](https://github.com/lepture/mistune) to render the markdown to HTML, and a single stylesheet to style these rendered files

It uses {Redis? LRU?} to cache rendered pages

## Possible Features

- setup.py? or requirements.txt?
- virtualenv?
- Search notes for key words
- Password lock certain notes
