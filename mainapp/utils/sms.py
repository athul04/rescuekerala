import calendar
import logging
import os

import environ
import requests
from dateutil import parser

from mainapp.models import SmsJob, Volunteer

logger = logging.getLogger("send_sms")

SMS_API_URL = os.environ.get("SMS_API")
API_USERNAME = os.environ.get("SMS_USER")
API_PASSWORD = os.environ.get("SMS_PASSWORD")


def sms_sender(smsjobid, **kwargs):
    smsjob = SmsJob.objects.get(id=smsjobid)
    if smsjob.has_completed is True:
        logger.info("Job already complete")
        return
    root = environ.Path(__file__) - 3
    environ.Env.read_env(root(".env"))

    district = kwargs["district"]
    _type = kwargs["type"]
    area = kwargs["area"]
    message = kwargs["message"]
    group = kwargs["group"]

    logger.info(
        "Starting sms job.\nDistrict: {}, Type: {}, Area: {}, Message: {} , Group: {}".format(
            str(district), str(_type), str(area), str(message), str(group)
        )
    )
    volunteers = Volunteer.objects.all()
    if district:
        volunteers = volunteers.filter(district=district)
    if area:
        volunteers = volunteers.filter(area=area)
    if group:
        volunteers = volunteers.filter(groups__in=[group])
    if not (district or area or group):
        smsjob.failure = "Incorrect Information Provided"
        logger.info(smsjob.failure)
        smsjob.has_completed = True
        smsjob.save()
        return
    logger.info("Filtered out {} Volunteers ".format(volunteers.count()))
    if _type != "consent":
        volunteers.filter(has_consented=True)
    fail_count = 0
    for volunteer in volunteers:
        if _type == "consent" or _type == "survey":
            timestamp = parser.parse(str(volunteer.joined))
            timestamp = calendar.timegm(timestamp.utctimetuple())
            # Preparing unique URL
            url = "http://keralarescue.in/c/" + str(volunteer.id) + "/" + str(timestamp)[-4:]
            message = "Thank you for registering as a volunteer on keralarescue. Please click here to confirm. " + url
            if _type == "survey":
                message = (
                    "Thanks keralarescue volunteer if willing to conduct damage assessment field survey, "
                    "Pls click on "
                    "the link to confirm. " + url
                )
        payload = {
            "username": API_USERNAME,
            "password": API_PASSWORD,
            "numbers": volunteer.phone,
            "message": message,
        }

        response = requests.get(SMS_API_URL, params=payload)
        logger.info("Got {} as response for {} - {}".format(response.text, volunteer.name, volunteer.phone))
        if "402" not in response.text:
            fail_count += 1

    smsjob.failure = "{} sms failed out of {}".format(fail_count, volunteers.count())
    logger.info(smsjob.failure)
    smsjob.has_completed = True
    smsjob.save()
