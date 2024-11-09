from django.db import models

# Create your models here.
class AdminLog(models.Model):
    log_id = models.IntegerField(primary_key=True)
    admin_id = models.IntegerField()
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin_log {self.log_id}: {self.admin_id} - {self.action}"

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
