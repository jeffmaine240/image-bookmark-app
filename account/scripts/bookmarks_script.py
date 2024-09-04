from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


def run():
    user = User.objects.get(username="jeffmaine")
    content_types = ContentType.objects.get(app_label="images", model="image")
    print(content_types)
    image_model = content_types.get_object_for_this_type(id=3)
    print(image_model)
