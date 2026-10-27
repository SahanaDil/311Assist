from flask import Flask, render_template, request
from records import load_records
from matching import find_by_case_number, find_by_address
from decisions import review_case, read_date
from datetime import date
app = Flask(__name__)
records = load_records()


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    mode = "case"
    matches = []
    searched = False
    error = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        mode = request.form.get("mode", "case")
        if not query:
            error = "Please enter a case number or street address."
        elif mode not in ("case", "address"):
            error = "Please use either supported search method; case number or street address."
        else:
            searched = True

            if mode == "case":
                matches = find_by_case_number(records, query)
            else:
                matches = find_by_address(records, query)
                matches.sort(
                    key=lambda record: (
                        read_date(record.get("Created Date Local")) or date.max
                    )
                )
            
    reviewed_matches = [
        {
            **record,
            "review": review_case(record),
        }
        for record in matches
    ]
    return render_template("index.html", query=query, mode=mode, matches=reviewed_matches, searched=searched, error=error,)