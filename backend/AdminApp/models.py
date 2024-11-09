from django.db import models

# Create your models here.
class Admin_log(models.Model):
    log_id = models.IntegerField(max_length=10, primary_key=True)
    admin_id = models.IntegerField(max_length=10)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def log_action(cls, admin_id, action):
        try:
            cls.objects.create(admin_id=admin_id, action=action)
            return True
        except Exception:
            return False
    
    def get_admin_logs(cls, admin_id):
        try:
            return cls.objects.filter(admin_id=admin_id).order_by('-timestamp')
        except Exception:
            return []
