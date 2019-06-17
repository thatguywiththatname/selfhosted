from flask import Flask, render_template
import pathlib, sys, flask_caching
import renderer, paths

# Where to look for the notes. Should point to the root of the repository
# Designed so that the Uni repo is cloned next to this "site" repo
NOTES_REPO = pathlib.Path("../../../Uni/")

# TODO: Write setup code for running under a domain name / subdomain
app = Flask(__name__)
cache = flask_caching.Cache(
    app,
    config={
        "CACHE_TYPE": "null" if sys.argv[-1] == "--no-cache" else "filesystem",
        "CACHE_DIR": "/tmp",  # TODO: Windows support
        "CACHE_DEFAULT_TIMEOUT": 300,
    },
)


@app.route("/")
@cache.cached()
def index():
    """Returns a list of years
    """
    year_nums = [
        int(y.split("year_")[1]) for y in paths.get_matching(NOTES_REPO, "year_*")
    ]
    return render_template("index.html", year_nums=year_nums)


@app.route("/<int:year_num>/")
@cache.cached()
def year_page(year_num):
    """Returns a list of units in that year
    """
    units = paths.get_matching(NOTES_REPO, f"year_{year_num}/notes/*")
    if units:
        return render_template(
            "year.html", title=f"Year {year_num}", year_num=year_num, unit_dirs=units
        )
    return render_template(
        "missing_content.html", year_num=year_num, missing_name="units"
    )


@app.route("/<int:year_num>/<unit_name>/")
@cache.cached()
def unit_page(year_num, unit_name):
    """Returns a list of notes taken for that unit in that year
    """
    note_titles = paths.get_note_titles(NOTES_REPO, year_num, unit_name)

    if note_titles:
        return render_template(
            "unit.html",
            title=unit_name,
            year_num=year_num,
            unit_name=unit_name,
            note_titles=note_titles,
        )

    return render_template(
        "missing_content.html",
        year_num=year_num,
        unit_name=unit_name,
        missing_name="notes",
    )


@app.route("/<int:year_num>/<unit_name>/<int:note_session>/")
@cache.cached()
def note_page(year_num, unit_name, note_session):
    """Returns a rendered version of the note
    """
    markdown_path = NOTES_REPO / f"year_{year_num}/notes/{unit_name}/{note_session}.md"
    try:
        note_html = renderer.render_target(markdown_path)
    except FileNotFoundError:
        # TODO: Redirect to 404 instead?
        return render_template("errors/404.html")
    return render_template(
        "note.html",
        title=f"{unit_name} - {note_session}",
        year_num=year_num,
        unit_name=unit_name,
        note_session=note_session,
        note_html=note_html,
    )


@app.errorhandler(404)
def page_not_found(e):
    # TODO: Return 404 code? how to handle other errs?
    return render_template("errors/404.html")


if __name__ == "__main__":
    app.run(debug=True)
