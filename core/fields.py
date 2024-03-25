from django.db import models
from django.forms.widgets import Select


class NigerianStateSelect(Select):
    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}
        attrs['class'] = 'nigerian-state-select' + (' ' + attrs['class'] if 'class' in attrs else '')
        super().__init__(attrs=attrs, *args, **kwargs)


class NigerianStateField(models.CharField):
    description = "A field representing a Nigerian state"

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.get_state_choices()
        kwargs['max_length'] = 100
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_state_choices():
        states = [
            ("AB", "Abia"),
            ("AD", "Adamawa"),
            ("AK", "Akwa Ibom"),
            ("AN", "Anambra"),
            ("BA", "Bauchi"),
            ("BY", "Bayelsa"),
            ("BE", "Benue"),
            ("BO", "Borno"),
            ("CR", "Cross River"),
            ("DE", "Delta"),
            ("EB", "Ebonyi"),
            ("ED", "Edo"),
            ("EK", "Ekiti"),
            ("EN", "Enugu"),
            ("GO", "Gombe"),
            ("IM", "Imo"),
            ("JI", "Jigawa"),
            ("KD", "Kaduna"),
            ("KN", "Kano"),
            ("KT", "Katsina"),
            ("KE", "Kebbi"),
            ("KO", "Kogi"),
            ("KW", "Kwara"),
            ("LA", "Lagos"),
            ("NA", "Nasarawa"),
            ("NI", "Niger"),
            ("OG", "Ogun"),
            ("ON", "Ondo"),
            ("OS", "Osun"),
            ("OY", "Oyo"),
            ("PL", "Plateau"),
            ("RI", "Rivers"),
            ("SO", "Sokoto"),
            ("TA", "Taraba"),
            ("YO", "Yobe"),
            ("ZA", "Zamfara"),
            ("AJ", "FCT Abuja")
        ]
        return states

    def formfield(self, **kwargs):
        defaults = {'widget': NigerianStateSelect}
        defaults.update(kwargs)
        return super().formfield(**defaults)
