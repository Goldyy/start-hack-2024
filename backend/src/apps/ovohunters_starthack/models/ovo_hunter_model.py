from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json



class OvoHunterModel(models.Model):
    """
    Model representing a Ovo hunter. A fraternization of moral hackers who travel to St. Gallen with trumpets and drums to build awesome shit in 36 hours!.

    Fields:         
        - name (CharField): The name of the Ovo-Hunter.
        - is_impressed_by (CharField): A person the Ovo-Hunter is almost certainly impressed by.
        - nickname (CharField): The nickname of the ovo-hunter.  
        - created_at (DateTimeField): The date and time when this ovo-hunter was created (auto-generated).
        - updated_at (DateTimeField): The date and time when this ovo-hunter was last updated (auto-generated).

    Methods:
        - __str__(): Returns a human-readable string representation of the Ovo-Hunter, which is its type.

    """

    name = models.CharField(max_length=250, null=True, blank=True)
    is_impressed_by = models.CharField(max_length=250, null=True, blank=True)
    nickname = models.CharField(max_length=250, null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_json(self):
        model_dict = {            
            'name': self.name,
            'is_impressed_by': self.is_impressed_by,
            'nickname': self.nickname,                 
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        return json.dumps(model_dict, indent=4, cls=DjangoJSONEncoder)

    def __str__(self):        
        model_dict = vars(self).copy()            
        model_dict.pop('_state', None)                
        if model_dict['created_at'] is not None:
            model_dict['created_at'] = model_dict['created_at'].isoformat() 
        else: 
            model_dict['created_at'] = None
        
        if model_dict['updated_at'] is not None:
            model_dict['updated_at'] = model_dict['updated_at'].isoformat() 
        else: 
            model_dict['updated_at'] = None      
        return json.dumps(model_dict, indent=4, cls=DjangoJSONEncoder)

