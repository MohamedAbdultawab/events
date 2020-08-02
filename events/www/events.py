import frappe


def get_context(context):
    """
        Context for events.html jinja2 template
    """
    context['docs'] = {}
    events = frappe.get_all('Custom Event',
        fields=['name', 'title', 'status', 'date'])
    for event in events:
        if event.get('status') not in context['docs']:
            context['docs'][event.get('status')] = []
        context['docs'][event.get('status')].append(event)
