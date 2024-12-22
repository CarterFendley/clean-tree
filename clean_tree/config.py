from __future__ import annotations
import os
from typing import Tuple

from pydantic import BaseModel, field_validator

class CleanTreeConfig(BaseModel):
    directories: Tuple[str, ...]
    # NOTE: No idea what the '...' syntax is needed, but the 'field_validator' fails without it: https://stackoverflow.com/questions/76758415/pydantic-issue-for-tuple-length

    max_display: int

    @field_validator('directories')
    @classmethod
    def validate_directories(cls, directories: Tuple[str]) -> Tuple[str]:
        directories = tuple(os.path.abspath(d) for d in directories)

        not_a_directory = []
        for d in directories:
            if not os.path.isdir(d):
                not_a_directory.append(d)

        if len(not_a_directory) != 0:
            msg = "The following paths are not directories:"
            for p in not_a_directory:
                msg += f"\n\t'{p}'"
            raise ValueError(msg)

        return directories