from django.forms import ModelForm, widgets, HiddenInput ,TextInput
from main.models import Lecturer
from django.utils.translation import gettext_lazy as _

class Lecturerform(ModelForm):
    user = HiddenInput()        
    class Meta:
        model = Lecturer
        fields = '__all__'
        widgets = {
            'user':HiddenInput(),
            'name':TextInput(attrs={'placeholder':'First Name'}),
            'last_name':TextInput(attrs={'placeholder':'Last Name'}),
        }
        labels = {
            'title':_('Name'),
            'name':_(''),
            'last_name':_(''),
            'lect_id':_('Teachers ID'),
            'course': _('Courses you teach'),
            'section':_('Sections you teach'),
        }

