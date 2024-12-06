# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import logging

from canway_action.controller import local_controller
from django.contrib.auth import get_user_model
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
import settings
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from .serializers import UserSerializer
from .tasks import base_task

logger = logging.getLogger("app")
class UserViewSet(ReadOnlyModelViewSet):
    """
    用户信息API
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], url_path="user_detail")
    def get_current_user(self, request):
        client = get_client_by_request(request)
        current_user = client.bk_login.get_user()
        return Response({'user': current_user})


class HealthzViewSet(ViewSet):
    """
    健康探测API
    """

    @action(detail=False, methods=["get"], url_path="healthz")
    def healthz(self, request, *args, **kwargs):
        """
        获取应用健康状态
        """
        return Response({"healthy": True})

    @action(detail=False, methods=["get"], url_path="ping")
    def ping(self, request, *args, **kwargs):
        """
        应用ping 接口
        """
        return Response("pong")


@api_view(['GET'])
def get_user(request):
    client = get_client_by_request(request)
    client2 = get_client_by_user(settings.LOCAL_PLUGIN_API_USER)
    # current_user = client.bk_login.get_user()
    token = request.COOKIES.get("bk_token", "")
    current_user = client2.usermanage.list_users()
    plugins = local_controller.get_all_action_plugins()
    my_action = local_controller.get_action_plugin("simple_action", "")
    input_schema, output_schema = my_action.schemas
    # token = client2.common_args['bk_token']
    result = my_action.execute(data={"token": token, "user": settings.LOCAL_PLUGIN_API_USER})

    logger.info(current_user)
    base_task.delay()
    print('base_task end')
    return Response(current_user)
