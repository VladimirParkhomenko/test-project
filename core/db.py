"""Mixins for Models"""


class UpdatableMixin(object):
    """
    Mixin for adding :func:`update()` with a list of allowed fields
    Class **must** contain subclass :class:`UpdateMeta` with
    :attr:`allowed_fields`

    """

    def update(self, **kwargs):
        """Update current instance with editable fields checking."""
        is_changed = False
        for name, value in kwargs.items():
            assert name in self.UpdateMeta.allowed_fields, \
                u"Field {} is not updatable".format(name)
            if getattr(self, name) != value:
                setattr(self, name, value)
                is_changed = True
        if is_changed:
            self.save()
        return is_changed
