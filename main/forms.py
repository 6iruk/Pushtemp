from django.forms import ModelForm, widgets, HiddenInput ,TextInput
from main.models import Teacher
from django.utils.translation import gettext_lazy as _

class Lecturerform(ModelForm):
    user = HiddenInput()        
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'user':HiddenInput(),
            'first_name':TextInput(attrs={'placeholder':'First Name'}),
            'last_name':TextInput(attrs={'placeholder':'Last Name'}),
        }
        labels = {
            'title':_('Name'),
            'first_name':_(''),
            'last_name':_(''),
            'email':_('E-mail'),
            'course': _('Courses you teach'),
            'section':_('Sections you teach'),
        }

