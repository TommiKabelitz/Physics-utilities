import itertools as it
import json
import os
import pprint
import yaml
import contextlib
import sys


def GetCombinations(detailSet):
    """
    Returns list of all possible dictionaries of values from a dictionary of whose
    values are lists.

    Nested lists will be treated as singular values and not permuted over.

    Arguments:
    detailSet - dict
        Dictionary whose values are lists

    Returns:
    combinations - list
        List of dictionaries with all keys maintained but with only singular values.

    example:
    {a:[1,2],b:[2],c:[[s,4]]} -> [{a:1,b:2,c[s,4]},
                                  {a:2,b:2,c[s,4]},}]

    """

    productValues = it.product(*[v for v in detailSet.values()])
    combinations = [dict(zip(detailSet.keys(), values)) for values in productValues]

    return combinations


def Load(parametersFile="", writeOut=False, *args, **kwargs):
    """
    Loads the parameters from parameters.yml.

    Arguments:
    parametersFile -- str: The parameters file to read
    writeOut       -- bool: Whether to write out the parameters dictionary
                           to the console when reading.
                           (for testing purposes)
    """

    # Opening and loading the yamml
    with open(parametersFile, "r") as f:
        parameters = yaml.safe_load(f)

    # Writing the details to the screen if specified
    if writeOut is True:
        pp(parameters)

    return parameters


def load_json(filepath: os.PathLike, encoding: str = "utf-8"):
    """Read from the given json file."""
    with open(filepath, "r", encoding=encoding) as f:
        return json.load(f)


def write_json(
    filepath: os.PathLike,
    dump_dict: dict,
    encoding: str = "utf-8",
    ensure_ascii: bool = False,
):
    """Write the given dictionary to the json file path."""
    with open(filepath, "w", encoding=encoding) as f:
        json.dump(dump_dict, f, ensure_ascii=ensure_ascii, indent=4)


def pp(toPrint, indent=4, stream=None, to_string=False):
    """
    Pretty printer, great for dictionaries.

    Literally just pprint.PrettyPrinter.pprint but with default arguments
    to simplify the call.

    Arguments:
    toPrint -- object: Object to be printed.
    indent -- int: Distance to indent each new level.
    stream -- fileObject: Where to print to. Default is sys.stdout.
    """
    printer = pprint.PrettyPrinter(indent=indent, stream=stream)

    if to_string:
        return printer.pformat(toPrint)
    else:
        printer.pprint(toPrint)


def StrFullReplace(basestr: str, replacementDict: dict, *args, **kwargs) -> str:
    """
    Replaces uppercase substrings in basestr with equivalent keys
    in replacementDict.

    Values in lists are joined with hypens, other types are simply
    converted using str().
    """
    replacedstr = basestr
    for substring, replacement in replacementDict.items():
        uppercase = substring.upper()

        if type(replacement) is list:
            replacedstr = replacedstr.replace(uppercase, str("-".join(replacement)), 1)
        else:
            replacedstr = replacedstr.replace(uppercase, str(replacement), 1)

    return replacedstr


def FindReplaced(inputDict: dict, replacementString: str, *args, **kwargs) -> dict:
    output = {}
    for key, value in inputDict.items():
        if type(value) is dict:
            check = FindReplaced(value, replacementString)
            # Only want to include if not empty
            if check:  # Empty dictionary returns False
                output[key] = check
        elif replacementString not in value:
            output[key] = value

    return output


def PrintDictKeys(d: dict, indent: int = 0, increment: int = 0):
    """
    Recursively prints keys in nested dictionaries in readable fashion.

    Arguments:
    d         -- dict: Dictionary to print keys of
    indent    -- int: Amount to indent printing
    increment -- int: Amount to increment each nest level. increment=0 will
                      indent based on length of keys at each level.
    """

    # Calculating increment amount if 0 is specified. Simply look for longest key
    actual_increment = increment
    if actual_increment == 0:
        for key in d.keys():
            # +1 is for the colon in print statement (looks a bit nicer)
            if len(key) + 1 > actual_increment:
                actual_increment = len(key) + 1

    # Looping through dictionary to print
    for key, value in d.items():
        # Printing the key and the type of what it contains
        print(f'{indent*" "}{key}: {type(value)}')
        # Recursively calling the function again when a nested dictionary is found.
        # Need to increase indent by the size of our keys or specified increment
        if type(value) is dict:
            indent += actual_increment
            PrintDictKeys(value, indent, increment)
            indent -= actual_increment  # And de-increment for next key


def DoFilenameReplace(fileDict: dict, replacementVals: dict, *args, **kwargs) -> dict:
    """
    Does the replacement of the given input files in place.

    Arguments:
    fileDict: dict
        Dictionary of files to replace. May contain nested dicts as long as they
        eventually result in strs
    replacementVals: dict
        Values to replace with
    """

    # Looping through dictionary
    for fileType, basePath in fileDict.items():
        if type(basePath) is dict:
            DoFilenameReplace(fileDict[fileType], replacementVals)
        else:
            # Doing replacement
            fileDict[fileType] = StrFullReplace(basePath, replacementVals)


class Metadata:
    def __init__(
        self, metadata_type: str, full_metadata: str, plain_text_metadata: str = None
    ):
        self.metadata_type = metadata_type
        self.full_metadata = full_metadata
        self.plain_text_metadata = plain_text_metadata
        if metadata_type == "t":  # Plain metadata
            self.plain_text_metadata = full_metadata

    def __str__(self):
        return self.full_metadata

    def __repr__(self):
        return self.full_metadata


class DummyFile(object):
    def write(self, x): pass

    
@contextlib.contextmanager
def suppress_stdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout
