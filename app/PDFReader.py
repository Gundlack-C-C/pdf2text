import os, subprocess


def pdf2text(file):
    folder = os.path.dirname(file)
    assert os.path.isfile(file), f"Invalid file. File does not exist [{file}]!"
    assert os.path.isdir(os.path.dirname(file)), f"Invalid file. Folder does not exist [{folder}]"
    args = ["pdftotext", '-enc', 'UTF-8', f"{file}", '-']
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.stdout.decode('utf-8')