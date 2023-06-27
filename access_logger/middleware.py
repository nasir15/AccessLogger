import json
from django.core.files.base import File
from django.contrib.auth.models import AnonymousUser
from access_logger.models import AccessLogs
from django.contrib.auth import get_user_model


class AccessLogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        body = None
        if 'api-token-auth' not in request.path:
            if 'json' in request.headers.get('Content-Type',{}):
                try:
                    body = json.loads(request.body.decode())
                    body = repr([(item, value) for item, value in body.items()])
                except KeyError as e:
                    body = None
                    raise e
            else:
                try:
                    if request.method == 'GET':
                        body = repr([(item, value if not isinstance(value, File) else value.name) for item, value in request.GET.items()])
                    if request.method == 'POST':
                        body = repr([(item, value if not isinstance(value, File) else value.name) for item, value in request.POST.items()])
                except KeyError as e:
                    body = None
                    raise e
        else:
            body = None

        response = self.get_response(request)

        file_params = None
        if request.FILES:
            file_params = ', '.join(['({})'.format(file_path) for file_path in request.FILES])

        view_name = ''
        try:
            view_name = request.resolver_match.func.__name__
        except:
            pass

        data = ''
        try:
            data = repr(response.data)
        except KeyError as e:
            print("e is ",e)
            raise e
        
        user_model = get_user_model()
        uuid = request.POST.get('uuid', None)
        if uuid:
            uuid = uuid.lower()
        AccessLogs.objects.create(
            url_path=request.path,
            view_name=view_name,
            method=request.method,
            host_ip=request.META.get('REMOTE_ADDR'),
            http_x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR'),
            query_params=body,
            form_data=body,
            uuid=uuid,
            file_params=file_params,
            accessed_by=request.user if type(request.user)==user_model else None,
            results = data
        )
        # Code to be executed for each request/response after
        # the view is called.

        return response
