from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Starting mailchimp audience registration process
def RegisterForNewsletter(user_email):
    # Authentication users mailchimp account
    try:
        mailchimp = Client()
        mailchimp.set_config({
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_DATA_CENTER
        })
        response = mailchimp.ping.get()
        print(response)

    except ApiClientError as error:
        # Authentication failed
        print("mailchimp account verification failed: {}".format(error.text))
        return False

    # Data required for mailchimp add audience api
    data = {
        "status": "subscribed",
        "email_address": user_email,
    }

    try:
        # adding user to newsletter
        response = mailchimp.lists.add_list_member(settings.MAILCHIMP_EMAIL_LIST_ID, data)
        print("response: {}".format(response))
        return True

    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return False
