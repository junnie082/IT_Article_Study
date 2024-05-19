from ias.models import AI

def get_recent_week():
    recent_instance = AI.objects.order_by('-create_date').first()
    return recent_instance.pk

