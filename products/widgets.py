from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileUnit(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = '/workspace/CI-MS4-Farm2Table/products/templates/custom_widget_templates/custom_clearable_file_unit.html'
