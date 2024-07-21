from django.shortcuts import render
from . models import Volunteer
import africastalking




def volunteer(request):
    context = {} 
    
    if request.method == "POST":
        person = Volunteer.objects.create(
            name = request.POST['name'],
            age = request.POST['age'],
            gender = request.POST['gender'],
            speciality = request.POST['speciality'],
            phone_number = request.POST['phone_number'],
            years_of_volunteering_experience = request.POST['years_of_volunteering_experience'],
            skills = request.POST['skills']
        )

        person.save()
        print('-----------step 1----')

        phone_number = phone_number
        message = 'Thank you for Volunteering, Kindly report at Nairobi Githurai as soon as possible and ensure you are well guard'

        #  Initialize the SDK
        username ='message_app'
        api_key = 'ec239632c120c9cbbe076998fe491a8bf3fac7dc0682b35b020f5e59ca187f53'
        africastalking.initialize(username, api_key)

        # Initialize a service e.g. SMS
        sms = africastalking.SMS

        # Use the service synchronously
        response = sms.send(message, [phone_number])
        volunteer_info =Volunteer.objects.get(id = person.id)

        context = {
            'name': volunteer_info.name,
            'gender':volunteer_info.gender,
            'speciality':volunteer_info.speciality,
            'years_of_volunteering_experience': volunteer_info.years_of_volunteering_experience,
            'skills':volunteer_info.skills

        }
    return render (request, 'volunteer.html',context)
