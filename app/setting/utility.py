from app import db
from app.setting.models import Setting


def get_setting(setting_name):
    value = Setting.query.filter_by(key=setting_name).first()
    return value


def save_setting(setting_name, value):
    new_setting = Setting(
        key=setting_name,
        value=value
    )
    db.session.add(new_setting)
    db.session.commit()
