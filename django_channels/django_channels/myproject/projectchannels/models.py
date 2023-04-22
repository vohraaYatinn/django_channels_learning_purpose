from django.db import models
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json

ORDER_CHOICES = {
    ("baking","baking"),
    ("cooking","cooking")

}
# Create your models here.
class order_Data(models.Model):
    order_seen = models.CharField(max_length=255)
    @staticmethod
    def given_order(id):
        instance=order_Data.objects.get(id=id)
        data={}
        data["order_seen"]=instance.order_seen
        return data

@receiver(post_save,sender=order_Data)
def order_stats_handler(sender, instance, created , **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data={}
        data["order_seen"]=instance.order_seen
        async_to_sync(channel_layer.group_send)(
            "order_%s" % instance.id,{
                'type': 'order_stats',
                'value': json.dumps(data)
            }
        )

