from reversion.middleware import RevisionMiddleware


class AuditMiddleware(RevisionMiddleware):
    """
    This class is in charge og auditing(logging) changes in models.
    As of 24/05/2018 it does nothing more than the reversion middleware.
    """
    pass
