"""ハンドラのレジストリ。@register でハンドラを名前登録する。"""

_HANDLERS = {}


def register(name):
    def deco(fn):
        _HANDLERS[name] = fn
        return fn
    return deco


def get_handler(name):
    return _HANDLERS.get(name)
