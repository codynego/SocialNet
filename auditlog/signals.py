from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from posts.models import Post
import logging
from .models import AuditLog


# Create your views here.

class Logger:
    def __init__(self, name):
        self.name = name

    def create_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        filehandler = logging.FileHandler(f"{self.name}s.log")
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

        return logger

@receiver([post_save, post_delete], sender=Post)
def post_log(sender, instance, **kwargs):
    user = instance.author
    created = kwargs.get('created', False)
    model_name = sender.__name__
    if kwargs.get("signal") == 'post_save':
        if created:
            action = "POST"
            details = f"{user} created a new post"
    else:
        action = "DELETED"
        details = f"{user} deleted a post id ({instance.id})"
    AuditLog.objects.create(user=user,
                            model_name=model_name,
                            action=action,
                            details=details)
    logger = Logger("post").create_logger()
    logger.info(details)