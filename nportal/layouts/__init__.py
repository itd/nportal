class MyLayout(object):
    page_title = 'Hooray! My App!'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.home_url = request.application_url

    def is_user_admin(self):
        return has_permission(self.request, 'manage')
