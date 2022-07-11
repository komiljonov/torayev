import json
from flask import Flask, request
from flask_cors import CORS
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

app = Flask(__name__)

CORS(app)

@app.route('/register', methods=["GET", "POST"])
def register():
    data = json.loads(request.data)
    name, number = data['name'], data['number']
    pipeline: Pipeline = Pipeline.objects.get(object_id=5559010)
    status: Status = Status.get_for(pipeline).get(object_id=49093348)
    new_lead: Lead = Lead(
        data={
            'name':f"Telegram HR Bot {number} {name} "
        }
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
    return "salom"



app.run()