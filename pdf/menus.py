"""Menus for PDF app"""
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from menu import Menu, MenuItem

from pdf.models import PDFRequest, Status
from pdf.cachemenuitem import CacheMenuItem


def distinct_requests():
    """
    Not all databases can do DISTINCT ON, this is a replacement for the command below
    PDFRequest.objects.filter(file__isnull=False, status=Status.DONE).distinct("filename")[:5]

    """
    files = set()
    data = []
    for entry in PDFRequest.objects.filter(file__isnull=False, status=Status.DONE):
        # pylint: disable=protected-access
        if entry.filename not in files:
            try:
                data.append(MenuItem(entry.filename, entry.file.url))
                files.add(entry.filename)
            # pylint: disable=bare-except
            except:
                continue
    return data


pdf_children = (
    MenuItem(_("Create new PDF"),
             reverse("pdf:new")),
    MenuItem(_("PDF Requests"),
             reverse("pdf:list")),
)

Menu.add_item("pdf", MenuItem(_("PDF"),
                              reverse("backend:index"),
                              children=pdf_children,
                              check=lambda request: request.user.is_authenticated))


Menu.add_item("files", CacheMenuItem(title=_("Files"),
                                     url=reverse("backend:index"),
                                     generate_function=distinct_requests,
                                     key=settings.PDF_CACHE_KEY,
                                     timeout=60 * 60))
