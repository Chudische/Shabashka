import os
from urllib.request import urlretrieve
from django.core.files import File
from .models import ShaUser, ShaUserAvatar

def update_avatar(backend, user, response, is_new=False, *args, **kwargs):

    if is_new and backend.name == "facebook":        
        image_url='https://graph.facebook.com/{0}/picture/?type=large&access_token={1}'.format(response['id'],response['access_token'])
        result = urlretrieve(image_url, f'{user.username}_fb_social.jpeg')        
        avatar = ShaUserAvatar.objects.create(
            user=user,            
            image=File(open(result[0], 'rb'))
        )
        avatar.save()       
    

