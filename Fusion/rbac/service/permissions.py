#!/usr/bin/python3.6
from django.conf import settings
from django_redis import get_redis_connection


class PermissionMixin(object):

    def __init__(self):
        self.redis_con = get_redis_connection()

    def init_permission(self, curret_user):
        """
        获取权限列表
        :param curret_user:
        :return:
        """
        permission_query = curret_user.roles.filter(permissions__isnull=False).values(
            "permissions__id",
            "permissions__title",
            "permissions__name",
            "permissions__url",
            "permissions__menu",
            "permissions__pid__id",
            "permissions__pid__url",
            "permissions__pid__title",
            "permissions__menu__id",
            "permissions__menu__title",
            "permissions__menu__icon"
        ).distinct()

        permission_dict={}
        menu_dict = {}
        for item in permission_query:
            permission_dict[item["permissions__name"]] = {
                "id": item["permissions__id"],
                "title": item["permissions__title"],
                "url": item["permissions__url"],
                "pid": item["permissions__pid__id"],
                "pid_title": item["permissions__pid__title"],
                "pid_url": item["permissions__pid__url"]
            }
            menu_id = item["permissions__menu__id"]
            if not menu_id:
                continue
            node = {"id": item["permissions__id"], "title": item["permissions__title"], "url":item["permissions__url"]}
            if menu_id in menu_dict:
                menu_dict[menu_id]['children'].append(node)
            else:
                menu_dict[menu_id] = {
                    "id": item["permissions__id"], "title": item["permissions__title"], "url": item["permissions__url"],
                    "children": [node,]
                }
        permission_user_key = curret_user.username+"@"+"permission_url"
        menu_user_key= curret_user.username+"@"+"menu_icon"
        self.redis_con.set(permission_user_key,permission_dict)
        self.redis_con.set(menu_user_key,menu_dict)








