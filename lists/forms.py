from django import forms
from lists.models import Item
EMPTY_ITEM_ERROR = 'No puede haber items vacíos'
class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {'text': forms.TextInput(attrs={
                        'placeholder': 'Nueva Tarea a realizar',
                        'class': 'form-control input-lg',}),
                  }
        error_messages = {
                'text': {'required': EMPTY_ITEM_ERROR}
        }