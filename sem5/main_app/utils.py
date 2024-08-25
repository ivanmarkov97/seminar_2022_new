from pathlib import Path


def get_config_dir():
    return Path(__file__).resolve().parent / 'configs'
