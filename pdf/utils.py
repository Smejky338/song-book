"""Utility functions"""
from time import time

from django.utils.translation import gettext_lazy

from pdf.models import PDFRequest, RequestType, Status


def request_pdf_regeneration(locale):
    """Requests automatic PDF regeneration if none is pending"""
    if not PDFRequest.objects.filter(type=RequestType.EVENT, status=Status.QUEUED, locale=locale):
        PDFRequest(type=RequestType.EVENT,
                   status=Status.QUEUED,
                   locale=locale,
                   filename=f"{gettext_lazy('songlist')}-{locale}").save()


class Timer:
    """Context manager for measuring time"""
    def __init__(self):
        self.duration = 0
        self.start = 0
        self.end = 0

    def __enter__(self):
        self.start = time()

    def __exit__(self, exit_type, value, traceback):
        self.end = time()
        self.duration = self.end - self.start
