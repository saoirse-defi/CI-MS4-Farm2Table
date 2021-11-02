from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class StoreClearableFileUnit(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'store/templates/store/custom_widget_templates/store_clearable_file_unit.html'
