from PS_AssetClasses import AssetClass as AC


class DescendantAware(object):
    """
    An abstract descendant-aware class.

    Once a subclass is created, it will be automatically included in the
    list returend by the get_descendants method. Subclasses may contain
    the following attribute:

    _abstract - a class attribute - if present and set to True, the subclass
        doesn't get to the task list. However, it's descendans do.

    """

    @classmethod
    def get_descendants(cls):
        """Get all the (direct and indirect) non-abstract descendants."""
        descendants = []
        for subcls in cls.__subclasses__():
            if not subcls.__dict__.get('_abstract'): # Check the current class only, not the ancestors.
                descendants.append(subcls)
            descendants.extend(subcls.get_descendants())
        return descendants


class AlwaysRelevant(object):
    is_relevant = staticmethod(lambda cfg: True)


def relevant_for_products(*products):
    """
    Factory for mixins that are relevant for particular products only.
    """
    class Abstract(object):
        is_relevant = staticmethod(lambda cfg: any(cfg[p.key] for p in products))
    return Abstract

# Shortcuts for often used relevance classes.
RelevantForEquities = relevant_for_products(*AC.get_equities())
RelevantForFixedIncome = relevant_for_products(*AC.get_fixed_income())
RelevantForRisk = relevant_for_products(*AC.get_risk())
