from rest_framework.serializers import ModelSerializer
from .models import Notification


class CreateNotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ("user","content","button_name","button_url")

class GetNotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ("id","sent_by","content","timestamp","button_name","button_url")