"""Menus for PDF app"""
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
    for entry in PDFRequest.objects.filter(file__isnull=False, status=Status.DONE).order_by("-created_date"):
        if entry.filename not in files:
            files.add(entry.filename)
            data.append(MenuItem(entry.filename, entry.file.url))
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
                                     key="MENUITEMS",
                                     timeout=60 * 60))
