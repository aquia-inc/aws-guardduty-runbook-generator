import re
from pathlib import Path


def chomp_keep_single_spaces(string):
    """This chomp cleans up all white-space, not just at the ends
    stolen with <3 from aws-allowlister
    """
    result = str(string)
    result = string.replace("\n", " ")  # Convert line ends to spaces
    # Truncate multiple spaces to single space
    result = re.sub(" [ ]*", " ", result)
    # Replace weird spaces with regular spaces
    result = result.replace(" ", " ")
    result = result.replace(u"\xa0", u" ")  # Remove non-breaking space
    result = re.sub("^[ ]*", "", result)  # Clean start
    return re.sub("[ ]*$", "", result)  # Clean end


def write_runbook(content, filename, directory, overwrite=None):
    """Writes finding runbook to a file
    Args:
        content (dict): JSON to write
        directory (str): File output location
        filename (str): File name
        overwrite (str): Overwrite files
    """
    p = Path(directory)
    if not p.is_dir():
        p.mkdir()

    # if we have not set overwrite and the file already exists, skip
    if not overwrite and Path(f"{p}/{filename}").is_file():
        pass
    else:
        with open(f"{p}/{filename}.md", 'w') as f:
            f.write(content)
            f.close()
            print(f"Wrote {directory}/{filename}.md")
