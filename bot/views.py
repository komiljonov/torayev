import json
from django.shortcuts import render
from django.http.response import JsonResponse
from amocrm.v2.tokens import default_token_manager as manager
from amocrm.v2 import Lead, Status, Pipeline, Contact
# Create your views here.

manager(
    "76e2ac7f-12a1-4ba1-8c94-64386fce59f6",
    'tvFfRm2hrZx77XXtUIggF4YnP9Bl3ALJzj87XKcOowogZIXtX2J0ZDTo60iCI5yQ',
    "kozimhonturaev",
    "https://example.com"
)

def make_data(name, number):
    return {
        'name': f'Web site lead {number} {name}',
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

def register(request):
    data = json.loads(request.body)
    
    name = data['name']
    number = data['number']

    pipeline: Pipeline = Pipeline.objects.get(object_id=5559010)
    status: Status = Status.get_for(pipeline).get(object_id=49093348)
    new_lead: Lead = Lead(
        data={
            'name':f"Web site lead {number} {name}"
        }
    )
    new_lead._data.update(
        {'custom_fields_values': [
            {
                'field_id': 801067,
                'field_name': 'Бизнес соҳа',
                'field_code': None,
                'field_type': 'text',
                'values': [
                    {
                        'value': 'Dasturlash'
                    }
                ]
            }
        ]}
    )
    new_lead.status = status
    new_lead.save()
    contact: Contact = Contact()
    contact._data = make_data(name, number)
    contact.save()
    new_lead.contacts.append(
        contact
    )
    new_lead.save()
    return JsonResponse({
        "ok": True
    })


def home(request):
    return render(request, 'index.html', )