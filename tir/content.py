from typing import Dict


class ContentObject(object):
    _required_meta = ['title', 'subtitle']

    def __init__(self, **meta: Dict):
        self.meta = meta
