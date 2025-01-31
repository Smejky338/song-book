"""Views for backend app"""
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView

from backend.forms import SongForm
from backend.models import Song
from backend.utils import regenerate_pdf, regenerate_prerender
from category.models import Category


def add_fields(song, authenticated: bool):
    """Adds additional fields to the JSON"""

    song['text'] = song["prerendered_web"]
    if authenticated:
        song['edit_url'] = reverse("chords:edit", kwargs={"pk": song["id"]})
        song['delete_url'] = reverse("chords:delete", kwargs={"pk": song["id"]})
    del song["prerendered_web"]


class SongListView(ListView):
    """Lists songs in the one page application"""
    model = Song
    template_name = 'songs/index.html'
    context_object_name = 'songs'

    FIELDS = ["id", "name", "capo", "author", "link", "prerendered_web"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        authenticated = self.request.user.is_authenticated

        songs = list(context_data['songs'].values(*self.FIELDS))

        for i, _ in enumerate(songs):
            songs[i]['number'] = i + 1
            add_fields(songs[i], authenticated)

        context_data['songs'] = json.dumps(songs, cls=DjangoJSONEncoder)
        return context_data


class IndexSongListView(SongListView):
    """Shows first available category"""

    def get_queryset(self):
        if Category.objects.count() > 0:
            slug = settings.DEFAULT_CATEGORY
            if slug and Category.objects.filter(slug=slug).exists():
                category = Category.objects.get(slug=slug)
            else:
                category = Category.objects.all()[0]
            return super().get_queryset().filter(categories__slug=category.slug)
        return super().get_queryset()


@method_decorator(login_required, name='dispatch')
class SongCreateView(SuccessMessageMixin, CreateView):
    """Creates new song"""
    form_class = SongForm
    model = Song
    template_name = 'songs/add.html'
    success_message = _("Song %(name)s was successfully created")
    success_url = reverse_lazy("backend:index")

    def get_success_url(self):
        regenerate_pdf(self.object)
        regenerate_prerender(self.object)
        return super().get_success_url()


@method_decorator(login_required, name='dispatch')
class SongUpdateView(SuccessMessageMixin, UpdateView):
    """Updates existing song"""
    form_class = SongForm
    model = Song
    template_name = 'songs/add.html'
    success_url = reverse_lazy("backend:index")
    success_message = _("Song %(name)s was successfully updated")

    def form_valid(self, form):
        if len(form.changed_data) > 0:
            regenerate_pdf(self.object)
            regenerate_prerender(self.object)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SongDeleteView(DeleteView):
    """Removes song"""
    model = Song
    template_name = "songs/confirm_delete.html"
    success_url = reverse_lazy("backend:index")
    success_message = _("Song %s was successfully deleted")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        regenerate_pdf(self.object)
        messages.success(self.request, self.success_message % self.object.name)
        return response


@method_decorator(login_required, name='dispatch')
class SongsDatatableView(BaseDatatableView):
    """API for datatables that returns all songs"""
    model = Song
    max_display_length = 500
    columns = ["name", "author", "capo"]
