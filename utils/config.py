import ConfigParser
from django.conf import settings


def get_config(section, option, filename='nthu_course.cfg'):
    '''Return a config in that section'''
    try:
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(settings.BASE_DIR + '/NTHU_Course/config/' + filename)
        return config.get(section, option)
    except:
        # no config found
        return None


def get_config_section(section, filename='nthu_course.cfg'):
    '''Return all config in that section'''
    try:
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(settings.BASE_DIR + '/NTHU_Course/config/' + filename)
        return dict(config.items(section))
    except:
        # no config found
        return {}
