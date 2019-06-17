from natsort import natsorted


def get_matching(path, pattern):
    """Find all dirs / files in path that match the given pattern
    Returns a naturally sorted list of directory / file names that match
    """
    return natsorted([p.name for p in path.glob(pattern)])


def get_note_titles(path, year_num, unit_name):
    """Iterates over all note .md files in the given dir and grabs the titles
    Returns a naturally sorted dict of note_num to note_title
    TODO: Is it possible for a dict to become "un-sorted"?
    """
    note_titles = {}
    notes_dir = path / f"year_{year_num}/notes/{unit_name}/"

    for note_file in natsorted(notes_dir.glob("*.md")):

        with open(note_file, "r") as in_file:
            first_line = in_file.readline()

        note_num = note_file.name.replace(".md", "")

        # Remove title markdown and newline char
        note_title = first_line.replace("# ", "")
        note_title = note_title.replace("\n", "")

        note_titles[note_num] = note_title.strip()

    return note_titles
