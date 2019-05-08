from json import JSONDecodeError

from django import forms
import json

ARE_YOU_SURE = 'Are you sure you uploaded the right file?'

class UpdateForm(forms.Form):
    elm_json = forms.FileField()

    def clean_elm_json(self):
        try:
            decoded_data = json.load(self.cleaned_data['elm_json'])
        except JSONDecodeError:
            raise forms.ValidationError('This is not valid JSON file please provide elm.json')

        try:
            if not isinstance(decoded_data["dependencies"]["direct"], dict):
                raise forms.ValidationError(f'Dependencies in wrong format. {ARE_YOU_SURE}')
            elm_version = decoded_data["elm-version"]
        except KeyError:
            raise forms.ValidationError(f'This is not valid elm.json. {ARE_YOU_SURE}')

        if elm_version != "0.19.0":
            raise forms.ValidationError('Elm Finder supports only Elm 0.19 and also contains only packages for this version of the language.')
        return decoded_data
