import json
import os, sys
import importlib  # module名を文字列で指定
# application_name = os.environ['APPLICATION_NAME']  # sample_application_name
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

# AccessToken = importlib.import_module(application_name).models.AccessToken

import requests
from django.shortcuts import render, render_to_response
from django.views import View
from django_qiita_analyzer.models import AccessToken


# TemplateViewを継承
from django.views.generic.base import TemplateView
from django.conf import settings



class RedirectView(TemplateView):
    # template名
    template_name = settings.REDIRECT_URL

    def get(self, request, **kwargs):
        """QiitaのOAUTH使ってリダイレクトされた情報取得"""
        if "code" in request.GET:
            # リダイレクトされた情報の中にある"code"を取得
            code = request.GET.get("code")
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code
        }
        req = requests.post("https://qiita.com/api/v2/access_tokens",
                            json.dumps(data).encode("utf-8"),
                            headers={"Content-Type": "application/json"})

        for key, value in req.json().items():
            if "token" in key:
                # query_paramが指定されている場合の処理
                token = value
                access_token = AccessToken.objects.create(token=token)
                access_token.save()
        context = {
            'token': token
        }
        return self.render_to_response(context)
