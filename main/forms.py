from django.forms import ModelForm, widgets, HiddenInput
from main.models import Lecturer
from django.utils.translation import gettext_lazy as _

class Lecturerform(ModelForm):
    user = HiddenInput()        
    class Meta:
        model = Lecturer
        fields = '__all__'
        widgets = {
            'user':HiddenInput()
        }
        labels = {
            'name':_('First name'),
            'last_name':_('Last name'),
            'lect_id':_('Teachers ID'),
            'course': _('Courses you teach'),
            'section':_('Sections you teach'),
        }

