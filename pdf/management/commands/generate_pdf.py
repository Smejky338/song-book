from argparse import ArgumentParser
from datetime import datetime
from math import ceil

import weasyprint
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.conf import settings
from django_weasyprint.utils import django_url_fetcher

from backend.views import fetch_all_songs
from pdf.models import PDFRequest, Status
from pdf.utils import Timer, generate_pdf

TEMPLATE = "pdf/index.html"


def update_status(request: PDFRequest, status: Status, generate_all=False):
    """Updates status of the request if it is in DB"""
    if not generate_all:
        request.status = status
        request.save()


class Command(BaseCommand):
    """Generates PDF according to the PDF requests"""
    help = 'Generates PDFs that were requested'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('requests',
                            metavar='Requests',
                            type=int,
                            nargs='?',
                            default="0",
                            help="Number of requests to process, will process all requests if not value is specified")
        parser.add_argument('--all',
                            action='store_true',
                            help="Regenerates PDF for all locales")

    def handle(self, *args, **options):
        total_duration = 0
        generate_all = options["all"]

        if generate_all:
            objects = [generate_pdf(locale=locale[0]) for locale in settings.LANGUAGES]
            num = len(settings.LANGUAGES)
        else:
            objects = PDFRequest.objects.filter(status=Status.QUEUED)
            if options["requests"] > 0:
                objects = objects[:options["requests"]]
            num = objects.count()

            if num == 0:
                return "No requests, doing nothing"

        for request in objects:
            if generate_all or request.songs.count() == 0:
                songs = fetch_all_songs(locale=request.locale)
            else:
                songs = request.songs
            sorted_songs = sorted(songs, key=lambda song: song.name)

            update_status(request, Status.IN_PROGRESS, generate_all)

            try:
                timer = Timer()
                with translation.override(request.locale), timer:
                    name = request.filename or self.default_filename()
                    print(f"Generating {name}.pdf")
                    string = render_to_string(template_name=TEMPLATE, context={
                        "songs": songs,
                        "sorted_songs": sorted_songs
                    })
                    weasyprint.HTML(
                        string=string,
                        url_fetcher=django_url_fetcher,
                        base_url=self.get_base_url()
                    ).write_pdf(f"{settings.STATIC_ROOT}/{name}.pdf")
                total_duration += timer.duration
                request.time_elapsed = ceil(timer.duration)
                update_status(request, Status.DONE, generate_all)
                print(f"Done in {request.time_elapsed} seconds")

            except:
                print("failed")
                update_status(request, Status.FAILED, generate_all)

        return f"Processed {num} requests in {ceil(total_duration)} seconds"

    def default_filename(self):
        return 'songlist-{at}'.format(
            at=datetime.now().strftime('%Y%m%d-%H%M'),
        )

    def get_base_url(self):
        """
        Determine base URL to fetch CSS files from `WEASYPRINT_BASEURL` or
        fall back to using the root path of the URL used in the request.
        """
        return getattr(
            settings, 'WEASYPRINT_BASEURL',
            reverse("chords:index")
        )