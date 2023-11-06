from django import forms


class_name = """inline-block bg-gray-50 border text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-36 pl-5 p-2 
dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"""

class DateRangeForm(forms.Form):
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': class_name + ' datepicker-start', 'placeholder': "Select Start date"}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': class_name + ' datepicker-end', 'placeholder': "Select End date"}))