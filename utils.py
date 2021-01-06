import os


def report_message(text, log_file):
    if not text.endswith("\n"):
        text = text + '\n'

    with open(log_file, 'a+') as file:
        file.write(text)


def clean_up_logs(log_file):
    if os.path.exists(log_file):
        os.remove(log_file)