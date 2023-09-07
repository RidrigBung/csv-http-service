import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from functions import is_allowed_file, check_folder, get_csv_list
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
    data = get_csv_list()
    return render_template("get_files_list.html", title=title, data=data)


if __name__ == '__main__':
    app.run(debug=True)
