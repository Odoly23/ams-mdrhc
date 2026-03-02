from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, HTML
from .models import RIR, RIRItem
from django_summernote.widgets import SummernoteWidget
from costum.models import Category, Brand, Model, Source

class DateInput(forms.DateInput):
    input_type = 'date'

class RIRForm(forms.ModelForm):
    description = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}))
    arrival_date = forms.DateField(widget=DateInput(), required=True)

    class Meta:
        model = RIR
        fields = ['rir_no', 'invoice_no', 'container_no', 'company', 'arrival_date', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row mt-4'
        self.helper.layout = Layout(
            Column('rir_no', css_class='col-md-4 my-2'),
            Column('invoice_no', css_class='col-md-4 my-2'),
            Column('container_no', css_class='col-md-4 my-2'),
            Column('company', css_class='col-md-6 my-2'),
            Column('arrival_date', css_class='col-md-6 my-2'),
            Column('description', css_class='col-12 my-2'),
            HTML("""
                <div class='d-flex justify-content-end  card-tools'>
                    <a href='#' class='btn btn-sm btn-warning mr-2' onclick='window.history.back()'><i class="fa fa-arrow-circle-left"></i>
                        Cancel
                    </a>
                    <button type='submit' class='btn btn-sm btn-success'>
                        <i class="fa fa-save"></i> Save
                    </button>
                </div>
            """)
        )

class RIRItemForm(forms.ModelForm):
    class Meta:
        model = RIRItem
        fields = [
            'category', 'brand', 'model', 'purchase_type', 'source', 'donor_name',
            'quantity', 'unit_cost', 'description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row mt-3'
        self.helper.layout = Layout(
            Column('category', css_class='col-md-4 my-2'),
            Column('brand', css_class='col-md-4 my-2'),
            Column('model', css_class='col-md-4 my-2'),
            Column('purchase_type', css_class='col-md-4 my-2'),
            Column('source', css_class='col-md-4 my-2'),
            Column('donor_name', css_class='col-md-4 my-2'),
            Column('quantity', css_class='col-md-4 my-2'),
            Column('unit_cost', css_class='col-md-4 my-2'),
            Column('description', css_class='col-12 my-2'),
            HTML("""
                <div class='d-flex justify-content-end py-3 gap-2'>
                    <a href='#' class='btn btn-warning' onclick=self.history.back()><i class='fa fa-arrow-left-square'></i> Cancel</a>
                    <button type='submit' class='btn btn-primary'><i class='fa fa-save'></i> Save</button>
                </div>
            """)
        )