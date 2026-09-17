"""
clope is a package for interacting with the Cantaloupe/Seed Office system,
split into the spotlight, snow, and prepick submodules.
"""

import importlib

__all__ = ["spotlight", "snow", "prepick"]


def __getattr__(name: str):
    """
    Lazily import submodules so that a partial install (e.g. clope[snow])
    can still import clope even when sibling modules' deps are absent.
    """
    if name in __all__:
        module = importlib.import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
