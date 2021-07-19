import datetime
from time import sleep
import requests
import smtplib


def findSlot(pincodes, age):
    result=""
    slot_available = 0
    for pincode in pincodes:
        date_object = datetime.date.today()
        date = f"{date_object.day}-{date_object.month}-{date_object.year}"
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.ok:
            response_json = response.json()
            if response_json["centers"]:
                for center in response_json["centers"]:
                    for session in center["sessions"]:
                        if (session["min_age_limit"] <= age and session["available_capacity"] > 0):     
                            result=result+f'Address: {center["address"]}\nState: {center["state_name"]}\nDistrict: {center["district_name"]}\nPincode: {center["pincode"]}\nFee Type:  {center["fee_type"]}\nvaccine: {session["vaccine"]}\nslots: {session["slots"]}\nDate: {session["date"]}\nAvailable slots capacity:  {session["available_capacity"]}\n\n\n'
                            slot_available = slot_available + 1
        else:
            print("No Response")
    if not slot_available:
        print("No Vaccination slot available")
    else:
        send_mail(result)


def send_mail(info):
    server = smtplib.SMTP("smtp.gmail.com")
    server.ehlo()
    server.starttls()
    server.ehlo()

    """
    If you are using Google's Gmail service to send mail. So we need some settings (if required) for google's security purposes. If those settings are not set up, then the following code may not work, if the google doesnot support the access from third-party app.
    To allow the access, we need to set 'Less Secure App Access' settings in the google account. If the two step verification is on, we cannot use the less secure access.
    To complete this setup, go to the Google's Admin Console, and search for the Less Secure App setup.
    """

    server.login("add email here", "add password here")
    subject = "Slot available for vaccine"
    body = f"Go to COWIN Offical Website https://www.cowin.gov.in and book a slot as fast as possible.\n\nInformation\n\n{info}"
    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail(
        'add email here',
        'add email here',
        msg
    )
    print("Email has been sent")
    server.quit()


pincodes = input(
    "Enter Pin codes of districts separated by space for which you want to get notified for slot availability:").split()
age = int(input("Enter age:"))
while(1):
    findSlot(pincodes, age)
    sleep(60)
