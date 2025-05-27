import os
import sys


def find_and_add_target_path(
    target_dir="BIA-Ghostcoder", start_dir=None, max_levels_up=6
):
    """
    Search for a directory with the specified name and add it to sys.path.
    If the directory is not found, raise FileNotFoundError.

    Args:
        target_dir (str): The name of the directory to search for (default: "BIA-Ghostcoder")
        start_dir (str): Directory to start searching from (default: current script's directory)
        max_levels_up (int): Maximum number of parent levels to search upwards

    Returns:
        str: The path of the found directory if successful.

    Raises:
        FileNotFoundError: If the target directory is not found.
    """
    if start_dir is None:
        start_dir = os.path.dirname(os.path.abspath(__file__))

    current_dir = start_dir

    # First search in current directory and its subdirectories
    for root, dirs, _ in os.walk(current_dir):
        if target_dir in dirs:
            path = os.path.join(root, target_dir)
            if path not in sys.path:
                sys.path.append(path)
            return path  # Return the path if found

    # If not found, search parent directories
    for _ in range(max_levels_up):
        current_dir = os.path.dirname(current_dir)
        if not current_dir or current_dir == os.path.dirname(current_dir):
            break  # Reached root directory

        for root, dirs, _ in os.walk(current_dir):
            if target_dir in dirs:
                path = os.path.join(root, target_dir)
                if path not in sys.path:
                    sys.path.append(path)
                return path  # Return the path if found

    # If not found after all searches, raise an exception
    raise FileNotFoundError(
        f"Directory '{target_dir}' not found in {start_dir} or its {max_levels_up} parent directories."
    )
