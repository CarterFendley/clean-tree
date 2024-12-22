import os
import subprocess
from typing import Optional

from .logging import get_logger
from .util import ChDir

logger = get_logger(__name__)

def rev_parse_show_top_level() -> Optional[str]:
    result = subprocess.run(
        args=['git', 'rev-parse', '--show-toplevel'],
        capture_output=True
    )

    if result.returncode == 128:
        # Not in git directory, return none
        return None
    elif result.returncode == 0:
        return result.stdout.decode().replace('\n', '')

    raise RuntimeError("Unexpected return code from git rev-parse: %s", result.returncode)

def validate_git_dir(path: str) -> bool:
    """
    Use `git rev-parse --is-inside-work-tree` to validate a git directory by supplying a `GIT_DIR` environment variable.

    Args:
        path (str): The path to set `GIT_DIR` to.

    Returns:
        bool: If `--is-inside-work-tree` returns true.
    """
    result = subprocess.run(
        ['git', 'rev-parse', '--is-inside-work-tree'],
        env={'GIT_DIR': path},
        capture_output=True,
    )

    return result.stdout.decode() == 'true\n'

def find_git_directories(directory: str) -> str:
    logger.debug("Walking directory: %s" % directory)

    git_dirs = []
    # for root, dirs, _, _ in os.fwalk(directory):
    for root, dirs, _ in os.walk(directory):
        for d in dirs: 
            if d == '.git':
                path = os.path.join(root, d)
                # if validate_git_dir(path):
                #     git_dirs.add(path)
                git_dirs.append(path)

    print(f"Found {len(git_dirs)} git repositories")
    for d in git_dirs:
        print(f"\t'{d}'")

    # os.fwalk()
    # 25.6 total -> list, no verification
    # 36.8 total -> list, w verification
    # 37.9 total -> set, w verification
    # 32.0 total -> set, no verification

    # os.walk()
    # 31.191 total -> list, no verification
    # 30.26 total -> set, no verification