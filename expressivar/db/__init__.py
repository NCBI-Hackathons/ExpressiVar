import os.path


def _get_module_path():
    return os.path.dirname(__file__)


def _get_data_dir():
    return os.path.join(_get_module_path(), 'data')


DEFAULT_PROMOTER_DB = os.path.join(_get_data_dir(), 'promoters.hg19')
