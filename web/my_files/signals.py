from functools import partial
import hashlib
import logging
import magic
#-
from django.conf import settings
#-
from website.tasks import create_thumbnail

_logger = logging.getLogger(__name__)


def get_file_hash(fhandle, block_size=65536):
    hasher = hashlib.sha1()
    for buf in iter(partial(fhandle.read, block_size), b''):
        hasher.update(buf)
    return hasher.hexdigest()


def file_updating(sender, instance, **kwargs):
    dirty = instance.get_dirty_fields()

    if 'databits' in dirty and bool(instance.databits):
        binary = instance.databits

        binary.open()
        guesser = magic.Magic(mime=True)
        mimetype = guesser.from_buffer(binary.read(2048))
        if ';' in mimetype:
            mimetype = mimetype.split(';')[0]
        instance.mimetype = mimetype

        binary.open()
        instance.filehash = get_file_hash(binary)


def file_updated(sender, instance, **kwargs):
    dirty = instance.get_dirty_fields()

    # Ignore thumbnail images.
    for name, _, _ in settings.IMAGE_SIZES:
        if 'image_' + name in dirty:
            return

    if 'databits' in dirty and bool(instance.databits):
        if instance.mimetype.startswith('image/'):
            for name, size, _ in settings.IMAGE_SIZES:
                create_thumbnail(
                        ('my_files', 'MyFile', instance.pk),
                        'databits', 'image_' + name, size)
