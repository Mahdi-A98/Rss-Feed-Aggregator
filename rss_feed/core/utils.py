# In the name of GOD

import ipaddress

from django.db import connection
from django.utils.timezone import now


class GetRequestData :
    def __init__(self, request, response=None) -> None:
        self.request = request
        self.response = response

    def get_ip_address(self, request):
        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)

        if ipaddr:
            ipaddr = ipaddr.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR', '').split(',')[0]

        possibles = (ipaddr.lstrip('[').split(']')[0], ipaddr.split(':')[0])

        for ip_addr in possibles:
            try:
                return str(ipaddress.ip_address(ip_addr))
            except ValueError:
                pass
        return ipaddr
        
    def get_request_data(self):
        req_data = {}
        req_data['ip_address'] = self.get_ip_address(self.request)
        req_data['method'] = self.request.method
        req_data['user'] = self.request.user.username if self.request.user else None
        req_data['status'] = self.response.status_code if self.response else None
        req_data['time'] = str(now())
        req_data['endpoint'] = self.request.get_full_path()
        return req_data
