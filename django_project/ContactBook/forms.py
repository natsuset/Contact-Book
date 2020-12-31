from .models import Information
from django.forms import ModelForm
      
class InfromationForm(ModelForm):
      class Meta:
        model = Information
        fields = "__all__"