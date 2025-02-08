import logging

class IgnoreBatchTranslationErrorFilter(logging.Filter):
    """
    Logging filter to ignore messages related to batch translation errors.
    """
    def filter(self, record):
        return "Batch translation error" not in record.getMessage()
