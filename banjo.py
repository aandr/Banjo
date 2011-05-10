import json

class Banjo:
    """
    jQuery proxy for Python

    >>> from banjo import b, js
    >>> b('#home').toggle()
    $("#home").toggle()
    >>> b.map(b('p.blue'), js.myJsMapFunc)
    $.map($("p.blue"), myJsMapFunc)
    >>> b('#home').css('color', b('#otherelement').css('color'));
    $("#home").css("color", $("#otherelement").css("color"))
    """
    
    def __init__(self, jquery_name = "$"):
        self._jquery_name = jquery_name
        self._list = []

    def __call__(self, *args):
        return BanjoChainElement(func_name = self._jquery_name, args = args)

    def __getattr__(self, key):
        parent = BanjoChainElement(func_name = self._jquery_name)
        return BanjoChainElement(parent = parent, func_name = key, args = None)

class JsVar:
    def __getattr__(self, key):
        return BanjoChainElement(func_name = key)

class BanjoChainElement:
    def __init__(self, parent = None, func_name = None, args = None):
        self.parent = parent
        self.func_name = func_name
        self.args = args

    def __getattr__(self, key):
        return BanjoChainElements(parent = self, func_name = key)

    def __call__(self, *args):
        self.args = args
        return self

    def __unicode__(self):
        def repr_arg(arg):
            # Handle Django HttpResponses without a Django dependency
            if hasattr(arg, 'content'):
                return json.dumps(unicode(arg))
            if isinstance(arg, BanjoChainElement):
                return unicode(arg)
            else:
                return json.dumps(arg)

        if self.args is None:
            args_js = u""
        else:
            args_js = u"(" + u", ".join((repr_arg(x) for x in self.args)) + u")"

        if self.parent is None:
            return u"%s%s" % (self.func_name, args_js)
        else:
            return u"%s.%s%s" % (unicode(self.parent), self.func_name, args_js)

    __str__ = __unicode__

b = Banjo()
js = JsVar()
