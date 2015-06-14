from django.conf import settings

DEFAULT_CLASS = getattr(settings, 'SMALL_UUID_CLASS', 'smalluuid.SmallUUID')
