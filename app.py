import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from functions import \
    is_allowed_file, check_folder, get_csv_list,\
    get_csv_file_data, is_exists, save_delimiter,\
    delete_csv_file_data
from constants import title, UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ограничение максимального размера файла в 64 мегабайт
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

pages = {"list of all files": "get_files",
         "load file": "load_file", "open file": "get_filename"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/v1/csv-management")
def home():
    return render_template("home.html", title=title, pages=pages)


@app.route("/api/v1/csv-management/load-file", methods=["GET", "POST"])
def load_file():
    if request.method == "POST":
        file = request.files["file"]
        delimiter = request.form["delimiter"]
        filename = secure_filename(file.filename)
        if not is_allowed_file(filename):
            return render_template("bad_input.html", title=title, filename=filename, error="wrong file extension")
        if is_exists(filename):
            return render_template("bad_input.html", title=title, filename=filename, error="file with that name is already exist")
        check_folder()
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        print(delimiter)
        save_delimiter(filename, delimiter)
        return render_template("successed-file-load.html", title=title, filename=filename)
    # request.method == "GET"
    return render_template("load-file-form.html", title=title)


@app.route("/api/v1/csv-management/select-file", methods=["GET", "POST"])
def get_filename():
    if request.method == "POST":
        filename_text = request.form["filename_text"]
        filename_select = request.form["filename_select"]
        if not filename_text:
            if not filename_select:
                return render_template("bad_input.html", title=title, filename="", error="empty input")
            else:
                filename = filename_select
        else:
            filename = filename_text
        if not is_exists(filename + ".csv"):
            return render_template("bad_input.html", title=title, filename=filename, error="no such file")
        return redirect(url_for("get_file", filename=filename))
    # request.method == "GET"
    files = os.listdir(UPLOAD_FOLDER)
    options = [filename.split('.')[0] for filename in files]
    options.insert(0, "")
    return render_template("get-filename-form.html", title=title, options=options)


# GET /files
@app.route("/api/v1/csv-management/files")
def get_files():
    files = get_csv_list()
    return render_template("get-files.html", title=title, files=files)


# GET files/<filename>
@app.route("/api/v1/csv-management/files/<filename>", methods=["GET", "POST"])
def get_file(filename):
    if request.method == "GET":
        filename += ".csv"
        data = get_csv_file_data(filename)
        return render_template("get-file.html", title=title, filename=filename, data=data)
    # if request.method == "POST":
    delete_csv_file_data(filename)
    return render_template("successed-file-delete.html", title=title, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
