from static.constants import ALLOWED_EXTENSIONS


def is_allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
