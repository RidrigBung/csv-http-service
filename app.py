import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from functions import title, UPLOAD_FOLDER, is_allowed_file
from static.constants import title, UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('index.html', title=title)


@app.route("/csv-management/load-file", methods=["GET", "POST"])
def load_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        if file and is_allowed_file(filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return render_template("successed_file_load.html", title=title, filename=filename)
        else:
            return render_template("failed_file_load.html", title=title, filename=filename)
    # request.method == "GET"
    return render_template("load_file.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
