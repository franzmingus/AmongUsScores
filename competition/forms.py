from django import forms

from .models import CompetitionModel


class AddPlayerForm(forms.ModelForm):

    class Meta:
        model = CompetitionModel
        fields = ['new_player']