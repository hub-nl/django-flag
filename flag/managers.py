from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
import settings
Q = models.Q
default_ftype_pk = getattr(settings,'DEFAULT_FLAG_TYPE_PK', 1)

class FlagTypeManager(models.Manager):
  '''
  Manager for flag type.
  '''
  def get_default_type(self, *args, **kwargs):
    '''
    Returns default type of valuation according to settings or else
    the one with pk
    '''
    default_ftype = self.get(pk=default_ftype_pk, *args, **kwargs)
    return default_ftype    

  def get_type(self, for_ftype=None, *args, **kwargs):
    '''
    Returns type according to the title if provided or else the default
    type.
    '''
    ftype=self.get_default_type(*args, **kwargs)
    ''' disable for the moment
    if for_ftype:
      ftype=self.get(slug=for_ftype, *args, **kwargs)
    else:
      ftype=self.get_default_type(*args, **kwargs)
    '''    
    return ftype
  
class FlagManager(models.Manager):
  def filter_for_obj(self, obj, ftype=None, *args, **kwargs):
    '''
    Filter the valuations according to the object.
    '''
    ctype, object_pk = ContentType.objects.get_for_model(obj), obj.pk    
    return self.filter(content_type=ctype, object_pk=object_pk, ftype=ftype, *args, **kwargs)
    
  def get_by_obj_client(self, request, obj=None, content_type=None, object_pk=None, *args, **kwargs):                    
    '''
    The instance of valuation which matches the provided object
    and client (user) info if exists. 
    '''
    is_authenticated = request.user.is_authenticated() 
    q_user = Q(user=request.user) if is_authenticated else Q()
    
    flags_for_obj = self.filter_for_obj(obj, *args, **kwargs)
    flags_for_obj_by_client = flags_for_obj.filter(q_user)        
    
    if flags_for_obj_by_client:
      return flags_for_obj_by_client[0]
    else:
      return None