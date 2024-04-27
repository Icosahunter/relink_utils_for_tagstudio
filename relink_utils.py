from pathlib import Path
import difflib
import filetype
import mimetypes
import hashlib

auto_link_threshold = 0.8

def relink(missing_file: str|Path, files_to_search: list[Path|str], missing_file_hash: str = None):
    """
        Try to find the path for a file that has changed place/name/contents.
        Tries "relink_perfect" and if that fails tries "relink_guess".
        Returns None if no suitable match is found.
    """
    new_path = relink_perfect(missing_file, files_to_search, missing_file_hash)
    if new_path is None:
        new_path = relink_guess(missing_file, files_to_search)
    return new_path

def relink_perfect(missing_file: str|Path, files_to_search: list[Path|str], missing_file_hash: str = None):
    """
        Try to find the path for a file that has changed place/name/contents.
        Finds the closest file that has the same hash, name, or preferably both.
        Returns None if no such file is found.
    """

    _files_to_search = [Path(x) for x in files_to_search]
    _missing_file = Path(missing_file)

    dist_sort = lambda x: path_distance(x, _missing_file)

    same_name = [x for x in _files_to_search if x.name == _missing_file.name]

    same_hash = []
    if missing_file_hash is not None:
        same_hash = [x for x in _files_to_search if hash_file(x) == missing_file_hash]

        if len(same_hash) > 0:
            same_hash_and_name = [x for x in same_hash if x in same_name]
            if len(same_hash_and_name) > 0:
                same_hash_and_name.sort(key = dist_sort)
                return same_hash_and_name[0]
            same_hash.sort(key = dist_sort)
            return same_hash[0]
    
    if len(same_name) > 0:
        same_name.sort(key = dist_sort)
        return same_name[0]
    
    return None

def relink_guess(missing_file: str|Path, files_to_search: list[str|Path]):
    """
        Try to find the path for a file that has changed place/name/contents.
        Compares files names, types, and path distances and returns the closest file that passes the auto_relink_threshold for similarity.
        Returns None if no such file is found.
    """

    _files_to_search = [Path(x) for x in files_to_search]
    _missing_file = Path(missing_file)

    weighted_files = []
    for file in _files_to_search:
        weighted_files.append((file, file_diff_index(_missing_file, file)))
        
    weighted_files = [x for x in weighted_files if x[1] >= auto_link_threshold]

    if len(weighted_files) == 0:
        return None
    
    weighted_files.sort(key = lambda x: x[1])
    return weighted_files[0][0]

def file_diff_index(file1: Path, file2: Path):
    """
        Calculates the simularity between two files by comparing their names, types, and distance from each other.
        Return value is normalized to between 0 and 1.
    """
    x1 = 1 / (1 + 0.1*path_distance(file1, file2))
    x2 = str_compare(file1.stem, file2.stem)
    x3 = ext_compare(file1, file2)
    return (x1 + x2 + x3) / 3

def path_distance(path1: Path, path2: Path):
    """
        Calculates the path distance between two files.
        This is the number of folders you would have to move the file through to move it to the same folder as the other, and +1 if the file names are different.
    """
    if path1.absolute() == path2.absolute():
        return 0

    p1parts = path1.absolute().parts
    p2parts = path2.absolute().parts
    i = 0
    while p1parts[i] == p2parts[i]:
        i += 1
    return len(p1parts[i:]) + len(p2parts[i:]) - 1

def str_compare(str1, str2):
    """
        Compares the similarity of two strings using Python's buit in difflib.
    """
    return difflib.SequenceMatcher(None, str1, str2).ratio()

def ext_compare(file1: Path, file2: Path):
    """
        Compares the similarity of two file types.
        Considers exact file extension, mimetype (media type), and if they are text files, in that order.
    """
    if file1.suffix == file2.suffix:
        return 1
    elif get_mimetype(file1) == get_mimetype(file2):
        return 0.9
    elif is_text(file1) and is_text(file2):
        return 0.5
    else:
        return 0

def get_mimetype(file: str|Path):
    """
        Get mimetype (media type), using the extension if it exists, and magic numbers if it doesn't.
    """
    if file.suffix != '':
        return mimetypes.guess_type(file)[0]
    else:
        return filetype.guess(file)

def is_text(file: str|Path):
    """
        Check if a file is text or binary.
    """
    try:
        with open(file, 'tr') as f:  # try to open file in text mode
            f.read()
            return True
    except:  # if fail then file is non-text (binary)
        return False

# Yoinked from Stack Overflow (nearly unedited): https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def hash_file(file: str|Path):
    """
        Returns a hash of the files contents.
    """
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks

    sha1 = hashlib.sha1()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()