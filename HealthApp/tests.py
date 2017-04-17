from django.test import TestCase

from django import forms

from HealthApp import validate


# Create your tests here.

class ValidateFormInput(TestCase):

    # phone number validations

    def test_phoneTooLong(self):
        try:
            validate.phone("123456789012")
        except forms.ValidationError as error:
            assert (error.code == 'Phone number is too long'), 'wrong error code'

    def test_phoneTooShort(self):
        try:
            validate.phone("123456789")
        except forms.ValidationError as error:
            assert (error.code == 'Phone number too short'), 'wrong error code'
    def test_phoneRoamingSpecifier(self):
        try:
            validate.phone("92345678901")
        except forms.ValidationError as error:
            assert (error.code == 'Phone number too long/ invalid roaming specifier'), 'wrong error code'

    def test_phoneWithNonAlphaNumeric(self):
        try:
            validate.phone("1234567890~")
        except forms.ValidationError as error:
            assert (error.code == 'Phone number is not a number'), 'wrong error code'

    def test_phoneWithLetter(self):
        try:
            validate.phone("((((((((((---))))))-123456789a")
        except forms.ValidationError as error:
            assert (error.code == 'Phone number contains a letter'), 'wrong error code'

    # social security number validations

    def test_ssnTooLong(self):
        try:
            validate.ssn("1234567890")
        except forms.ValidationError as error:
            assert (error.code == 'More than 9 digits'), 'wrong error code'

    def test_ssnWithNonNumber(self):
        try:
            validate.ssn("12345678~")
        except forms.ValidationError as error:
            assert (error.code == 'Contains non-number'), 'wrong error code'

    def test_ssnTooShort(self):
        try:
            validate.ssn("12345678")
        except forms.ValidationError as error:
            assert (error.code == 'Less than 9 digits'), 'wrong error code'

    # zip code validations

    def test_zipTooLong(self):
        try:
            validate.zip("123456")
        except forms.ValidationError as error:
            assert (error.code == 'More than 5 digits'), 'wrong error code'

    def test_zipWithNonNumber(self):
        try:
            validate.zip("1234~")
        except forms.ValidationError as error:
            assert (error.code == 'Contains non-number'), 'wrong error code'

    def test_zipTooShort(self):
        try:
            validate.zip("1234")
        except forms.ValidationError as error:
            assert (error.code == 'Less than 5 digits'), 'wrong error code'
