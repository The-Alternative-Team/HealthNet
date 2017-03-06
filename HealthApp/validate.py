from django import forms

def phoneNumber(phone_number):
    phone_number = phone_number.replace('-', '')
    digit_counter = 0
    for digit in phone_number:
        digit_counter += 1
        if digit_counter > 10 :
            raise forms.ValidationError(
                'Invalid phone number.',
                code='phone number is too long'
            )
        if digit.isalpha():
            raise forms.ValidationError(
                'Invalid phone number.',
                code='phone number contains a letter'
            )
    if not phone_number.isdigit():
        raise forms.ValidationError(
            'Invalid phone number.',
            code='phone number is not a number'
        )
    return int(phone_number)

def email(email_address):
    at_sign_present = False
    at_sign_index = 0
    period_present = False
    index = 0
    for character in email_address:
        if index == 0:
            if character == '@':
                raise forms.ValidationError(
                    'Invalid email address.',
                    code='@ at index 0'
                )
        if ( not character.isalpha() and not character.isdigit()
             and not character == '@' and not character == '.'):
            raise forms.ValidationError(
                'Invalid email address.',
                code='illegal character in address'
            )
        if character == '@':
            if at_sign_present:
                raise forms.ValidationError(
                    'Invalid email address.',
                    code='multiple @'
                )
            at_sign_present = True
            at_sign_index = index
        if at_sign_present:
            if character == '.' and index == at_sign_index + 1:
                raise forms.ValidationError(
                    'Invalid email address.',
                    code='invalid email server'
                )
        if character == '.':
            period_present = True
        index += 1
    if not period_present:
        raise forms.ValidationError(
            'Invalid email address.',
            code='invalid mail server'
        )
    return email_address


def SSN(social):
    social = social.replace('-','')
    index = 0
    for digit in social:
        index += 1
        if index > 9:
            raise forms.ValidationError(
                'Invalid SSN',
                code='too many digits'
            )
        if not digit.isdigit():
            raise forms.ValidationError(
                'Invalid SSN',
                code='contains non-number'
            )
    if index < 9:
        raise forms.ValidationError(
            'Invalid SSN',
            code='less than 9 digits'
        )
    return int(social)