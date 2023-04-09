"""Django signal handlers, see apps.py

Warning: Becareful with what you do in this file because the functions are used
         in blog_posting migrations.
         Django migrations is different from the normal operation.
         I think thumbnail creation (backgroud tasks) is not working.
"""
from functools import partial
import hashlib
import logging
#-
from django.conf import settings
import magic
#-
from website.tasks import create_thumbnail
from .models import MyFile

_logger = logging.getLogger(__name__)


def get_file_hash(fhandle, block_size=65536):
    """Get hash value of a file
    """
    hasher = hashlib.sha1()
    for buf in iter(partial(fhandle.read, block_size), b''):
        hasher.update(buf)
    return hasher.hexdigest()


def schedule_for_deletion(field, files):
    """Get storage and file id
    """
    if not field:
        return
    files.append((field.storage, field.name))


def file_updating(sender, instance, **kwargs):
    """On file change, update hash and mimetype
    """
    dirty = instance.get_dirty_fields()

    if 'databits' in dirty and bool(instance.databits):
        if instance.id:
            old_instance = MyFile.objects.get(id=instance.id)
            old_files = []
            schedule_for_deletion(old_instance.databits, old_files)
            schedule_for_deletion(old_instance.image_xs, old_files)
            schedule_for_deletion(old_instance.image_sm, old_files)
            schedule_for_deletion(old_instance.image_md, old_files)
            schedule_for_deletion(old_instance.image_lg, old_files)
            instance._old_databits = old_files # pylint:disable=protected-access

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
    """On file change, create lower resolution images
    """
    dirty = instance.get_dirty_fields()

    # Ignore thumbnail images.
    for name, _, _ in settings.IMAGE_SIZES:
        if 'image_' + name in dirty:
            return

    if 'databits' in dirty and bool(instance.databits):
        old_databits = getattr(instance, '_old_databits', [])
        for storage, name in old_databits:
            storage.delete(name)

        if instance.mimetype.startswith('image/'):
            for name, size, _ in settings.IMAGE_SIZES:
                create_thumbnail(
                        ('my_files', 'MyFile', instance.pk),
                        'databits', 'image_' + name, size)


def file_deleted(sender, instance, **kwargs):
    """On file delete, delete all files
    """
    if instance.databits:
        instance.databits.storage.delete(instance.databits.name)
    if instance.image_xs:
        instance.image_xs.storage.delete(instance.image_xs.name)
    if instance.image_sm:
        instance.image_sm.storage.delete(instance.image_sm.name)
    if instance.image_md:
        instance.image_md.storage.delete(instance.image_md.name)
    if instance.image_lg:
        instance.image_lg.storage.delete(instance.image_lg.name)
