#emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
#ex: set sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Parameter representation"""

__docformat__ = 'restructuredtext'

from mvpa.misc.state import Collectable

class Parameter(Collectable):
    """This class shall serve as a representation of a parameter.

    It might be useful if a little more information than the pure parameter
    value is required (or even only useful).

    Each parameter must have a value. However additional property can be
    passed to the constructor and will be stored in the object.

    BIG ASSUMPTION: stored values are not mutable, ie nobody should do

    cls.parameter1[:] = ...

    or we wouldn't know that it was changed

    Here is a list of possible property names:

        min   - minimum value
        max   - maximum value
        step  - increment/decrement stepsize
    """

    def __init__(self, default, name=None, doc=None, **kwargs):
        """Specify a parameter by its default value and optionally an arbitrary number
        of additional parameters.

        TODO: :Parameters: for Parameter
        """
        self.__default = default

        Collectable.__init__(self, name, doc)

        if __debug__:
            if kwargs.has_key('val'):
                raise ValueError, "'val' property name is illegal."

        # XXX probably is too generic...
        for k, v in kwargs.iteritems():
            self.__setattr__(k, v)


    def resetvalue(self):
        """Reset value to the default"""
        Collectable.reset(self)
        self._value = self.__default

class KernelParameter(Parameter):
    """Just that it is different beast"""
    pass
