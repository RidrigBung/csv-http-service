import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from functions import is_allowed_file, check_folder, get_csv_list, get_csv_file_data
from constants import title, UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ограничение максимального размера файла в 64 мегабайт
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html", title=title)


@app.route("/csv-management/load-file", methods=["GET", "POST"])
def load_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        if file and is_allowed_file(filename):
            check_folder()
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return render_template("successed_file_load.html", title=title, filename=filename)
        else:
            return render_template("failed_file_load.html", title=title, filename=filename)
    # request.method == "GET"
    return render_template("load_file.html", title=title)


@app.route("/csv-management/get_files_list")
def get_files_list():
    files = get_csv_list()
    return render_template("get_files_list.html", title=title, files=files)


@app.route("/csv-management/get_file_data", methods=["GET", "POST"])
def get_filename():
    if request.method == "POST":
        filename_text = request.form["filename_text"]
        filename_select = request.form["filename_select"]
        if not filename_text:
            if not filename_select:
                return render_template("bad_filename.html", title=title, error="empty input")
            else:
                filename = filename_select
        else:
            filename = filename_text
        filename += ".csv"
        check_folder()
        files = os.listdir(UPLOAD_FOLDER)
        if filename not in files:
            return render_template("bad_filename.html", title=title, error="no such file")
        return redirect(url_for("get_file_data", filename=filename))
    # request.method == "GET"
    files = os.listdir(UPLOAD_FOLDER)
    options = [filename.split('.')[0] for filename in files]
    return render_template("get_filename.html", title=title, options=options)


@app.route("/csv-management/get_file_data/<filename>")
def get_file_data(filename):
    data = get_csv_file_data(filename)
    return render_template("get_file_data.html", title=title, filename=filename, data=data)


if __name__ == '__main__':
    app.run(debug=True)
