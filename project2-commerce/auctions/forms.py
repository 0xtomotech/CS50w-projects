from django import forms

from .models import Category


class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '5', 'cols': '50'}))
    bid = forms.DecimalField(widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'}))
    image_url = forms.URLField(widget=forms.URLInput(), required=False)
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Choose a category",
                                        required=False)
    new_category = forms.CharField(required=False, label="Optional: new category")


class BidForm(forms.Form):
    bid_amount = forms.DecimalField(widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'}), label="Place Bid")


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'cols': '50'}), label="")


class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())