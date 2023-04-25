from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


@register.generator('news:thumbnail')
class Thumbnail(ImageSpec):
    processors = [ResizeToFill(394, 257)]
    format = 'webp'
    options = {'quality': 80}
