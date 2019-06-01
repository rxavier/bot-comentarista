import re


def sanitizer(raw_string):

    """Replace newlines with period and space"""
    comment_process = re.sub("\n+", ".", raw_string)

    """Add space after any punctuation if missing"""
    comment_process = re.sub("(?<=[?.!:,;])(?=[^\\s])(?![.!?/0-9]|com|org|net|gub|edu|uy|blogspot)",
                             " ", comment_process)

    """Remove space before punctuation"""
    comment_process = re.sub(r'\s([?.!,;]+(?:\s|$))', r'\1', comment_process)

    """Remove period following any kind of punctuation"""
    comment_process = re.sub("(?<=[?!¿¡,;])\\.(?![.])", "", comment_process)

    """Add space after ellipsis if missing"""
    comment_process = re.sub("\\.{2-3}(?!\\s)", "... ", comment_process)

    """End string with period if not available"""
    if re.search("[.!:?\\-]", comment_process[-1]) is None:
        comment_process = comment_process + "."

    return comment_process
