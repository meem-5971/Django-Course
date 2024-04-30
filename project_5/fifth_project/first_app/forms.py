from django import forms
from django.core import validators

class contactForm(forms.Form):
    # name=forms.CharField(label="User Name")
    # file=forms.FileField()
    # email=forms.EmailField(label="User Email")
    # age=forms.IntegerField(label="Age")
    # cgpa=forms.FloatField(label="CGPA")
    # balance=forms.DecimalField()
    # check=forms.BooleanField()
    # birthday=forms.DateField()
    # appointment=forms.DateTimeField()
    # CHOICES=[('S','Small'),('M','Medium'),('L','Large')]
    # size=forms.ChoiceField(choices=CHOICES)
    # TOPPINGS=[('P','Papperomi'),('M','Mushroom'),('B','Beef')]
    # pizza=forms.MultipleChoiceField(choices=TOPPINGS)

    #using widgets and attributes
    name=forms.CharField(label="User Name", help_text="length mus be within 70 characters",required=False,widget=forms.Textarea(attrs={'id':'text_area','class':'class1','placeholder':'Enter Name'}))
    age=forms.CharField(widget=forms.NumberInput)
    birthday=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    appointment=forms.DateTimeField(widget=forms.DateInput(attrs={'type':'datetime-local'}))
    CHOICES=[('S','Small'),('M','Medium'),('L','Large')]
    size=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
    TOPPINGS=[('P','Papperomi'),('M','Mushroom'),('B','Beef')]
    pizza=forms.MultipleChoiceField(choices=TOPPINGS,widget=forms.CheckboxSelectMultiple)


# class StudentData(forms.Form):
#     name=forms.CharField(widget=forms.TextInput)
#     email=forms.CharField(widget=forms.EmailInput)
#     # def clean_name(self):
#     #     valname=self.cleaned_data['name']
#     #     if len(valname)<5:
#     #         raise forms.ValidationError("Name must be at least 5 characters")
#     #     return valname
    
#     # def clean_email(self):
#     #     valmail=self.cleaned_data['email']
#     #     if '.com' not in valmail:
#     #         raise forms.ValidationError("Email must contain .com")
#     #     return valmail

# #alternative
#     def clean(self):
#         cleaned_data=super().clean()
#         valname=self.cleaned_data['name']
#         valmail=self.cleaned_data['email']
#         if len(valname)<5:
#             raise forms.ValidationError("Name must be at least 5 characters")
#         if '.com' not in valmail:
#             raise forms.ValidationError("Email must contain .com")


#using validators
def len_check(value):
    if len(value)<10:
        raise forms.ValidationError("Text must be at least 10 characters")
class StudentData(forms.Form):
    name=forms.CharField(validators=[validators.MaxLengthValidator(10,message="Name must be at most 10 characters"),validators.MinLengthValidator(3, message='Name must be at least 3 characters') ])
    text=forms.CharField(widget=forms.TextInput,validators=[len_check])
    email=forms.CharField(widget=forms.EmailInput,validators=[validators.EmailValidator(message="Enter a valid email address")])
    age=forms.IntegerField(validators=[validators.MaxValueValidator(40, message="Age must be less than 40"),validators.MinValueValidator(18,message="Age must be greater than 18")])
    file=forms.FileField(validators=[validators.FileExtensionValidator(allowed_extensions=['pdf','png'],message='This must be a png or pdf file')])

class PasswordValidationProject(forms.Form):
    name=forms.CharField(widget=forms.TextInput)
    passwrd=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data=super().clean()
        username=self.cleaned_data['name']
        val_pass=self.cleaned_data['passwrd']
        con_pass=self.cleaned_data['confirm_password']
        if(val_pass !=con_pass):
            raise forms.ValidationError("Passwords do not match")
        if(len(username)<3):
            raise forms.ValidationError("Username must be at least 3 characters")