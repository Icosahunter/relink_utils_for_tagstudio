# Relink Utils

`relink_utils.py` contains utilities for finding a file that has moved, been renamed, or edited, based on it's previous file path and (optionally) hash.
These utilities were created for [TagStudio](https://github.com/TagStudioDev/TagStudio), but the interface is generic and it could easily be used elsewhere.
It has only one dependency, filetype, for determining file mimetype (media type) if the extension is missing.
Run `test.py` to display example results using the included test files in the `test/` directory.