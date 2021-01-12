import os


def report_message(text, log_file):
    """

    :param text: The text you want to be logged
    :param log_file: the file you want to log to
    :return: nothing
    """

    """
    Adding extra \n to the message in case it doesn't have one
    """
    if not text.endswith("\n"):
        text = text + '\n'

    """
    Opening the file with append command and writing the message
    """
    with open(log_file, 'a+') as file:
        file.write(text)


def clean_up_logs(log_file):
    """
    :param log_file: The file you want to delete
    :return: nothing
    """

    """
    If the file exists, delete it
    """
    if os.path.exists(log_file):
        os.remove(log_file)
