"""turayev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from amocrm.v2.tokens import default_token_manager as manager
from amocrm.v2 import Lead, Status, Pipeline, Contact

def make_data(name, number):
    return {
        'name': f'Telegram bot lead {number} {name}',
        'responsible_user_id': 8095414,
        'group_id': 0,
        'created_by': 8095414,
        'updated_by': 8095414,
        'created_at': 1657108850,
        'updated_at': 1657108850,
        'closest_task_at': None,
        'is_deleted': False,
        'is_unsorted': False,
        'custom_fields_values': [
            {
                'field_name': 'Телефон',
                'field_code': 'PHONE',
                'field_type': 'multitext',
                'values': [
                    {
                        'value': number,
                        'enum_code': 'MOB'
                    }
                ]
            }
        ],
        'account_id': 30111892,
    }


manager(
    "76e2ac7f-12a1-4ba1-8c94-64386fce59f6",
    'tvFfRm2hrZx77XXtUIggF4YnP9Bl3ALJzj87XKcOowogZIXtX2J0ZDTo60iCI5yQ',
    "kozimhonturaev",
    "https://example.com"
)






















def register( request):
        print(request.data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bot.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
