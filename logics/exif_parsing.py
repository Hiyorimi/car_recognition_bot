"""Handles parsing of exif image data."""

import datetime as dt
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS


def get_exif(content_or_filename):
    """Returns exif data."""
    image = Image.open(content_or_filename)
    image.verify()
    return image._getexif()


def get_exif_geotagging(exif) -> dict:
    """Gets exif data related to geo coordinates."""
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def get_datetime_orig_exif_tag(exif_data) -> str:
    """Extracts exif data related to time when photo was taken."""
    for (idx, tag) in TAGS.items():
        if tag == 'DateTimeOriginal':
            if idx not in exif_data:
                raise ValueError("No EXIF DateTimeOriginal found")
            return exif_data[idx]
    raise ValueError("No EXIF DateTimeOriginal found")


def get_photo_was_taken_at(exif_data) -> dt.datetime:
    """Extracts the time photo was taken at as datetime."""
    datetime_orig = get_datetime_orig_exif_tag(exif_data)
    photo_was_taken_at = dt.datetime.strptime(
        datetime_orig,
        '%Y:%m:%d %H:%M:%S',
    )
    return photo_was_taken_at
