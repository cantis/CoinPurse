from app import db
from app.setting.models import Setting


def get_setting(setting_name, default='none'):

    value = Setting.query.filter_by(key=setting_name).first()

    if value:
        return value

    if not value and default != 'none':
        return default

    if not value and default == 'none':
        return None


def save_setting(setting_name, value):
    new_setting = Setting(
        key=setting_name,
        value=value
    )
    db.session.add(new_setting)
    db.session.commit()
