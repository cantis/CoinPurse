from flask import session

from web import db
from web.models import Setting


def get_setting(setting_name, default='none'):

    # check if a setting exists in session already
    if session.get(setting_name):
        temp = session[setting_name]
        return temp

    # session doesn't have it = get it from db
    setting = Setting.query.filter_by(key=setting_name).first()

    if setting:
        session[setting_name] = setting.value
        return setting.value

    if not setting and default != 'none':
        return default

    if not setting and default == 'none':
        return None


def save_setting(setting_name, value):
    """ Add or update a setting value """
    setting_exists = Setting.query.filter_by(key=setting_name).first()
    if setting_exists:
        setting_exists.value = value
    else:
        new_setting = Setting(
            key=setting_name,
            value=value
        )
        db.session.add(new_setting)
    db.session.commit()

    # Save the value into session
    session[setting_name] = value


def clear_setting_cache():
    ''' Clear values in the session, call this as the user logs in to clear any previous session data. '''
    for key in list(session.keys()):
        session.pop(key)
