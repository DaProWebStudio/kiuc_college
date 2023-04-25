from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


@register.generator('news:thumbnail')
class Thumbnail(ImageSpec):
    processors = [ResizeToFill(378, 300)]
    format = 'webp'
    options = {'quality': 80}


@register.generator('news:image326')
class Image326(ImageSpec):
    processors = [ResizeToFill(326, 300)]
    format = 'webp'
    options = {'quality': 80}


@register.generator('news:image354')
class Image354(ImageSpec):
    processors = [ResizeToFill(354, 300)]
    format = 'webp'
    options = {'quality': 65}
    
    
@register.generator('user:image300')
class Image300(ImageSpec):
    processors = [ResizeToFill(354, 300)]
    format = 'webp'
    options = {'quality': 75}