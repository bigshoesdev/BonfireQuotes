from django.contrib.admin import AdminSite
from django.conf.urls import url
from django.shortcuts import render


class CustomAdminSite(AdminSite):
    site_header = "Inspire"
    site_title = "Inspire Portal"
    index_title = "Welcome to Inspire"

    def get_urls(self):
        urls = super(CustomAdminSite, self).get_urls()
        custom_urls = [
            url(r'schedule/post', self.admin_view(self.admin_schedule_post), name="schedule_post"),
        ]
        return urls + custom_urls

    def admin_schedule_post(self, request):
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            'title': self.index_title
        }

        request.current_app = self.name

        return render(request, 'admin/schedule_post.html', context)


admin_site = CustomAdminSite(name='admin')
