import json 

class PostHandler:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.method == 'POST':
            try:
                request.POST = json.loads(request.body)
            except:
                pass

        response = self.get_response(request)
        return response