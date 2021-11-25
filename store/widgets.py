from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class StoreClearableFileUnit(ClearableFileInput):
    clear_checkbox_label = _('')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'store/custom_widget_templates/store_clearable_file_unit.html'
