from django.views.generic import DetailView

from blog.models import Post


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        context['comments'] = comments
        return context
