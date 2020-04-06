#!/usr/bin/python3.6
import re
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from django.conf import settings
from rest_framework_jwt.utils import jwt_decode_handler
from jwt.exceptions import ExpiredSignatureError, InvalidAlgorithmError
from django.http import JsonResponse


class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        redis_con = get_redis_connection()
        current_url = request.path
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None
        #获取token值
        token = request.META.get('HTTP_TOKEN')
        if token:
            try:
                token_user = jwt_decode_handler(token)
                permission_key = token_user.get("username")+"@"+"permission_url"
                menu_key = token_user.get("username") +"@"+"menu_icon"
                permission_urls = eval(redis_con.get(permission_key))
                menu__icon = eval(redis_con.get(menu_key))
                url_record = []
                flag = False
                for item in permission_urls.values():
                    reg = "^%s$" % item['url']
                    if re.match(reg, current_url):
                        flag = True
                        request.current_select_permission = item["id"] or item["pid"]
                        if not item["pid"]:
                            url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                        else:
                            url_record.extend([
                                {'title': item['pid_title'], 'url': item['pid_url']},
                                {'title': item['title'], 'url': item['url'], 'class': 'active'},
                            ])
                        request.breadcrumb = url_record
                        break
                if not flag:
                    return JsonResponse({"status": 401, "message": "无权访问"})

            except ExpiredSignatureError as e:
                return JsonResponse({"status":500, "message":"token was 已经过期"})
            except InvalidAlgorithmError as e:
                return JsonResponse({"status":401, "message":"token 认证失败"})

