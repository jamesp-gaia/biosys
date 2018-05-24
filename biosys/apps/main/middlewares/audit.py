from reversion.middleware import RevisionMiddleware


class AuditMiddleware(RevisionMiddleware):
    """
    This class is in charge og auditing(logging) changes in models.
    As of 24/05/2018 it does nothing more than the reversion middleware but with the atomic turned off.
    Setting the atomic to True make one unit test fails
     test_species_observation.TestSpeciesNameFromNameID.test_wrong_id_rejected_upload
    Also there's potential issue if the django ATOMIC_REQUESTS is not set to True.
    see: https://github.com/etianen/django-reversion/issues/624#issuecomment-362413142
    """
    atomic = False

