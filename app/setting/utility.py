from flask import session

from app import db
from app.setting.models import Setting


def get_setting(setting_name, default='none'):
    setting = Setting.query.filter_by(key=setting_name).first()

    if setting:
        return setting.value

    if not setting and default != 'none':
        return default

    if not setting and default == 'none':
        return None


def save_setting(setting_name, value):
    """ Add or update a setting value """

    # check if a setting exists in session already
    


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

    session[setting_name] = value
