from amocrm.v2.tokens import default_token_manager as manager
from amocrm.v2 import Lead, Status, Pipeline, Contact


manager(
    "76e2ac7f-12a1-4ba1-8c94-64386fce59f6",
    'tvFfRm2hrZx77XXtUIggF4YnP9Bl3ALJzj87XKcOowogZIXtX2J0ZDTo60iCI5yQ',
    "kozimhonturaev",
    "https://example.com"
)



# leads: list[Lead] = Lead.objects.all()

# leads = [lead for lead in leads]

lead: Lead = Lead.objects.get(object_id=35945645)

# print(lead)
print(lead.__dict__)
# contacts: list[Contact] = lead.contacts

# for contact in contacts:
#     print(contact._data)

# leads.reverse()
# for lead in leads:
#     contacts: list[Contact] = lead.contacts
#     for contact in contacts:
#         print(contact._data)
#     break

