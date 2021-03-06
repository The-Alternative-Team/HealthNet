"""
validate

Module that includes global methods for validating user input on forms.

=== Methods ===

phoneNumber -- If the inputted phone number is determined invalid, raises ValidationError
               with error code detailing why the phone number was determined invalid. A valid phone
               number will be returned as an integer. If a valid phone number is inputted with
               hyphens, they will be removed automatically so the phone number can be returned as
               an integer that adheres to the SQLite database infrastructure. 

    :parameter (string) phone_number - The string inputted into a phone number field by a user.
    :returns (integer) Phone number that is confirmed valid and is formatted for the SQLite database.

SSN ---------- If the inputted social security number is determined invalid, raises ValidationError
               with error code detailing why the social security number was determined invalid. A valid
               social security number will be returned as an integer. If a valid social security number
               is inputted with hyphens, they will be removed automatically so the social security number
               can be returned as an integer that adheres to the SQLite database infrastructure.

    :parameter (string) social - The string inputted into a social security number field by a user.
    :returns (integer) Social security number that is confirmed valid and is formatted for the SQLite database.
    
zip ---------- If the inputted zip code is determined invalid, raises ValidationError
               with error code detailing why the zip code was determined invalid. A valid
               zip code will be returned as an integer.

    :parameter (string) zip - The string inputted into the zip code field by a user.
    :returns (integer) Zip code that is confirmed valid.

"""

from datetime import datetime, timedelta
from django.forms import ValidationError


def phone(phone_number):
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace('(', '')
    phone_number = phone_number.replace(')', '')
    digit_counter = 0
    for digit in phone_number:
        digit_counter += 1
        if digit_counter > 11:
            raise ValidationError(
                'Invalid phone number.',
                code='Phone number is too long'
            )
        if digit.isalpha():
            raise ValidationError(
                'Invalid phone number.',
                code='Phone number contains a letter'
            )
    if digit_counter < 10:
        raise ValidationError(
            'Invalid phone number',
            code='Phone number too short'
        )
    if not phone_number.isdigit():
        raise ValidationError(
            'Invalid phone number.',
            code='Phone number is not a number'
        )
    if digit_counter == 11 and phone_number[0] != '1':
        raise ValidationError(
            'Invalid phone number.',
            code='Phone number too long/ invalid roaming specifier'
        )
    return int(phone_number)


def ssn(social):
    social = social.replace('-', '')
    index = 0
    for digit in social:
        index += 1
        if index > 9:
            raise ValidationError(
                'Invalid SSN',
                code='More than 9 digits'
            )

        if not digit.isdigit():
            raise ValidationError(
                'Invalid SSN',
                code='Contains non-number'
            )
    if index < 9:
        raise ValidationError(
            'Invalid SSN',
            code='Less than 9 digits'
        )
    return int(social)


def zip(zip):
    index = 0
    for digit in zip:
        index += 1
        if index > 5:
            raise ValidationError(
                'Invalid zip code',
                code='More than 5 digits'
            )
        if not digit.isdigit():
            raise ValidationError(
                'Invalid zip code',
                code='Contains non-number'
            )
    if index < 5:
        raise ValidationError(
            'Invalid zip code',
            code='Less than 5 digits'
        )
    return int(zip)


def birthday(birth_day):
    current_day = datetime.now().date()
    age = current_day - birth_day
    if age <= timedelta(days=0):
        raise ValidationError(
            'Invalid birthday',
            code='Born in future'
        )
    return


def appointment(start_time, end_time):

    if start_time == '' or end_time == '':
        raise ValidationError(
            'Blank dateTime',
            code='Please enter valid start and end times.'
        )

    start_dtime = datetime.strptime(start_time,'%Y-%m-%dT%H:%M')
    end_dtime = datetime.strptime(end_time,'%Y-%m-%dT%H:%M')

    current_time = datetime.now()
    appointment_duration = end_dtime - start_dtime

    if appointment_duration < timedelta(minutes=0):
        raise ValidationError(
            'Invalid end time',
            code='Appointment starts after it ends'
        )

    if appointment_duration == timedelta(minutes=0) or \
            appointment_duration > timedelta(hours=5) or \
            appointment_duration < timedelta(minutes=15):
        raise ValidationError(
            'Invalid duration',
            code=
            'Appointment duration must be between 15 minutes and 5 hours inclusive'
        )

    if start_dtime <= current_time :
        raise ValidationError(
            'Invalid start time',
            code='Appointment starts in the past'
        )
    return
