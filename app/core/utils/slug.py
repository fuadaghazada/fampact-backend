from django.utils.text import slugify as django_slugify

SLUG_MAP = {
    'Ə': 'e',
    'ə': 'e',
    'Ö': 'o',
    'ö': 'o',
    'Ü': 'u',
    'ü': 'u',
    'I': 'i',
    'ı': 'i',
    'Ğ': 'g',
    'ğ': 'g',
    'Ş': 's',
    'ş': 's',
    'Ç': 'c',
    'ç': 'c',
}


def slugify(value):
    value = str(value)

    # Re-map some strings to avoid important characters being stripped.
    for k, v in SLUG_MAP.items():
        value = value.replace(k, v)

    return django_slugify(value, allow_unicode=True)


def replace_alphabet(title):
    for value in title:
        if value in ["ə", "Ə"]:
            title = title.replace(value, "e")
        elif value in ["ı"]:
            title = title.replace(value, "i")
    return title


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`
    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    field = replace_alphabet(field)
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug
