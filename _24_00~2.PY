import requests
from datetime import datetime
import time, smtplib

MY_LAT = 25.672939  # Your latitude
MY_LONG = -100.309731  # Your longitude
my_email1 = "Test1.Omega1000@gmail.com"
# password = "password"
their_email2 = "Test1.Omega1000@gmail.com"
time_to_rerun_again_in_seconds = 2

print(f"My current Latitude: {MY_LAT}")
print(f"My current Longitude: {MY_LONG}")

def the_ISS_is_overhead_now():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(f"iss_latitude: {iss_latitude}")
    print(f"iss_longitude: {iss_longitude}")

    #Your position is within +5 or -5 degrees of the ISS position.
    if abs(iss_latitude - MY_LAT) <= 5.0 and abs(iss_longitude - MY_LONG) <= 5.0:
        return True

def it_is_dark_now_at_your_location():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        # "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json?lat=25.672939&lng=-100.309731&formatted=0", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_time_my_location = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time_my_location = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour_now_my_location = time_now.hour
    # print(f"The data type of hour_now_my_location is: {type(hour_now_my_location)}")

    if time_now >= sunset_time_my_location or time_now <= sunrise_time_my_location:
        print(f"The Hour of the time now is: {hour_now_my_location}")
        return True

# def location_and_time_updated_checker():
#     if hour_now_my_location >= sunset_time_my_location and hour_now_my_location <= sunrise_time_my_location:
#         if abs(iss_latitude - MY_LAT) <= 5.0 and abs(iss_longitude - MY_LONG) <= 5.0:    # ORRRR: if 20.6 <= iss_latitude <= 30.6:       Code to execute if x is within 5.0 points of y
#             # return True                                                                                # Same thing: if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
while True:
    time.sleep(time_to_rerun_again_in_seconds)
    if the_ISS_is_overhead_now() and it_is_dark_now_at_your_location():
        global time_now
        subject = f"Subject: Look up in the sky!! It's the International Space Station!\n\n"
        body = f"It should be dark enough while it's passing over your head, to be able to see it, at your location of: {MY_LAT}, {MY_LONG}. The date and time is: {time_now}"  # letter_content.replace("[NAME]", name)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email1, password=password)
            connection.sendmail(from_addr=my_email1,
                                to_addrs=their_email2,
                                msg=f"{subject}{body}")

# TODO: These things:
# If the ISS is close to my current position, check.
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



#Attribution and credit for the sunrise_time_my_location and sunset_time_my_location API functionality goes rightfully to: https://sunrise-sunset.org/api