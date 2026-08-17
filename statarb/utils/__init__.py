"""Shared utilities: config loading, path resolution, and legacy constants.

Config is read only through the loader here so that the config hash travels with every
generated artifact. A science module never opens a yaml file directly and never hardcodes
a threshold, a cost, a weight, or a unit conversion. SPEC Part K: every threshold and
factor lives in config, and changing 1 regenerates downstream under a new hash.
"""
