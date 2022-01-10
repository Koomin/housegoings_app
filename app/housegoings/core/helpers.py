import re
import unicodedata


def normalize_string(string):
    return re.sub(" +", " ", unicodedata.normalize("NFKD", string))