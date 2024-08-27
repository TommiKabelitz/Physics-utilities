import os

import numpy as np

import many_read

read_many_files = many_read.reader.read_many_files


def read_binary_files(
    file_list: list[str], nbytes_per_file: int, check_files: bool = False
) -> np.ndarray:
    max_len = max(len(s) for s in file_list)
    file_string = "".join(f"{s:<{max_len}}" for s in file_list)

    if check_files:
        for f in file_list:
            if not os.path.exists(f):
                if os.path.getsize(f) != nbytes_per_file:
                    raise ValueError(
                        f"File {f} does not have the expected size {nbytes_per_file}"
                    )

    buffer = np.zeros(nbytes_per_file * len(file_list), dtype=np.uint8)
    read_many_files(
        n_files=len(file_list),
        bytes_per_file=nbytes_per_file,
        all_names_len=len(file_string),
        file_names=file_string,
        buffer=buffer,
    )
    return buffer
