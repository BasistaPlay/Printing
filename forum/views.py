from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from forum.models import Thread, Post
from forum.forms import ThreadForm, PostForm
from django.shortcuts import get_object_or_404, redirect

class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'
    context_object_name = 'threads'

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = self.get_object()
            post.created_by = request.user
            post.save()
            return redirect('forum:thread_detail', pk=self.get_object().pk)
        return self.get(request, *args, **kwargs)


class ThreadCreateView(CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'thread_form.html'
    success_url = reverse_lazy('forum:thread_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)