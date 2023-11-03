# In the name of GOD

from .utils import GetRequestData

import json
import logging


api_logger = logging.getLogger('API_logger')


class LogMiddleWare :
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.log_info = {}

    def __call__(self, request):
        
        response = self.get_response(request)
        getdata = GetRequestData(request, response)
        self.log_info.update(getdata.get_request_data())
        api_logger.info(json.dumps(self.log_info))
        return response

    def process_exception(self, request, exception):
        """
        called when a view raise an exception
        """
        getdata = GetRequestData(request)
        self.log_info.update(getdata.get_request_data())
        self.log_info['exception'] = str(exception)
        api_logger.error(msg=json.dumps(self.log_info))
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        called before django calls the view
        """
        return None

    def process_template_response(self, request, response):
        """
        called just after the view has finished executing
        """
        return response
        