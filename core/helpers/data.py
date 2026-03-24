"""
    Helper functions to handle data operations.
"""

def getter(subject, key, defaultValue = None):
    """
        Safely fetch key from dictionary or object, without
        throwing errors. Can set a default for failed fetches.

        :param subject: [obj|dict]
        :param key: [str]
        :param defaultValue: [*]
    """
    if isinstance(subject, dict):
        return subject.get(key, defaultValue)
    if isinstance(subject, object):
        return getattr(subject, key, defaultValue)
    return defaultValue

