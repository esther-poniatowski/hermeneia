"""
Initialization logic and public interface for the `hermeneia` package.

See Also
--------
importlib.metadata.version
    Function to retrieve the version of a package.
PackageNotFoundError
    Exception raised when the package is not found in the environment.

Examples
--------
To programmatically retrieve the package version:

    >>> import hermeneia
    >>> hermeneia.__version__
    '0.1.0'
"""

from importlib.metadata import version, PackageNotFoundError
import platform

try:
    if __package__ is None:  # erroneous script execution
        raise PackageNotFoundError
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = ["info", "__version__"]


def info() -> str:
    """Format diagnostic information on package and platform.

    Returns
    -------
    str
        Resulting value produced by this call.
    """
    return f"{__package__} {__version__} | Platform: {platform.system()} Python {platform.python_version()}"
