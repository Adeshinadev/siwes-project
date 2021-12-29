from django.shortcuts import render, redirect
from mailjet_rest import Client
import os
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Uploads
from django.http import HttpResponse
from django.core.exceptions import FieldDoesNotExist, FieldError
import xlwt


api_key = 'df8fce202586aceb5291a8de0c983811'
api_secret = 'd49727836520ca9030654f2ede11c410'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


# Create your views here.
def home(request):
    return render(request, 'home.html')


def admin_login(request):
    return render(request, 'admin-login.html')


@login_required(login_url='make_login')
def dashboard(request):
    uploads = Uploads.objects.all()
    return render(request, 'index.html', {'uploads': uploads})


def Login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                user_obj = User.objects.get(username=request.POST.get('email'))
                print(user_obj, 'ooooo')
                return redirect(dashboard)
        messages.info(request, 'password or username incorrect')
        return render(request, 'admin-login.html')
    else:
        return render(request, 'admin-login.html')


def upload_details(request):
    if request.method == 'POST':
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "support@themobiele.com",
                        "Name": "Student Submission"
                    },
                    "To": [
                        {
                            "Email": "Adeshinex4u@gmail.com",
                            "Name": "passenger 1"
                        }
                    ],
                    "TemplateID": 3318226,
                    "TemplateLanguage": True,
                    "Subject": "Student Submission",
                    "Variables": {
                        "name_of_student": request.POST['first_name'],
                        "matric_no": request.POST['first_name'],
                        "phone_no": request.POST['matric_no'],
                        "email": request.POST['email'],
                        "department": request.POST['Department'],
                        "faculty": request.POST['faculty'],
                        "doa": request.POST['doa'],

                    }
                }
            ]
        }

        result = mailjet.send.create(data=data)
        # print(result.status_code)
        # print(result.json())
        # print()
        messages.info(request, 'Form Submitted')
        return render(request, 'home.html')


def admin_permit(user):
    if user.is_staff:
        return True
    else:
        return False


@login_required(login_url='Login')
@user_passes_test(admin_permit, login_url='Login')
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="User.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'Siwes Data')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    if request.POST['field'] == 'all':

        columns = ['Full name', 'Matric No.' 'Email Address', 'Faculty', 'Department', 'Info']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        try:
            rows = Uploads.objects.all()
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        except FieldError or rows is None:
            # messages.info(request, 'invalid arguments')
            return render(request, '404page.html')

    elif request.POST['field'] == 'Department':

        columns = ['Full name', 'Matric No.', 'Email Address', 'Faculty', 'Department', 'Info']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        try:
            rows = Uploads.objects.filter(department=request.POST['field'])
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        except FieldError or rows is None:
            # messages.info(request, 'invalid arguments')
            return render(request, '404page.html')

    elif request.POST['field'] == 'Faculty':

        columns = ['Full name', 'Matric No.' 'Email Address', 'Faculty', 'Department', 'Info']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        try:
            rows = Uploads.objects.filter(faculty=request.POST['key_word'])
            print(rows, request.POST['key_word'])
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        except FieldError or rows is None:
            # messages.info(request, 'invalid arguments')
            return render(request, '404page.html')
