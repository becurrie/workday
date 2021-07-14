import os

from dateutil.parser import (
    parse,
)
from pathlib import (
    Path,
)

from src.conf.config import (
    config,
)
from src.exceptions import (
    ValidationError,
)


def validate_directory(value):
    """Validates that the ``value`` specified is a valid directory.
    """
    path = Path(value)

    if not path.is_dir():
        raise ValidationError(
            title="Not A Directory",
            message="Please enter a valid directory path.",
        )


def validate_repository(value):
    """Validates that the ``value`` specified is a valid git repository.
    """
    path = Path(value)
    git = Path(os.path.join(value, ".git"))

    if path.is_dir() and not git.is_dir():
        raise ValidationError(
            title="Not A Valid Repository",
            message="Please enter a valid git repository path.",
        )


def validate_repository_duplicate(value):
    """Validates that the ``value`` specified isn't already a duplicate
    tracked repository.
    """
    if value in config.repositories:
        raise ValidationError(
            title="Duplicate Repository",
            message="That repository is already being tracked.",
        )


def validate_time(value):
    """Validates that the ``value`` specified is a valid time value.
    """
    try:
        parse(value)
    except Exception as exc:
        raise ValidationError(
            title="Invalid Time",
            message="Please enter a valid time string.",
        )
