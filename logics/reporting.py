import datetime as dt
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def get_when_description(taken_at: dt.datetime) -> str:
    """Returns datetime in **kancelyarnii stil**."""
    return dt.datetime.strftime(taken_at, '%d %B %Y года в %H:%M:%S')
