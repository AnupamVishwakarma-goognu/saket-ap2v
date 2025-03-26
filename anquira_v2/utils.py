from anquira_v2.anquira_handlers import ReferenceModeChoices
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def tat_algorithm(enquiry_date,enquiry_attended_dt):
    import datetime
    import pytz
    utc=pytz.UTC

    tat_period_in_minutes = 60
    tat_percent = 100
    start_hours = 9
    end_hours = 18
    try:
        # if datetime() > 9am and < 6pm then consider 9am
        office_hours_start = utc.localize(datetime.datetime.now().replace(hour=start_hours, minute=0)) #(Morning 9 AM)
        office_hours_end_previous_day = utc.localize(datetime.datetime.now().replace(hour=end_hours, minute=0) - datetime.timedelta(days=1))# (Evening 6 PM)
        print("Office Hour Start : ",str(office_hours_start))
        print("Office Hours End Privious Day : ",str(office_hours_end_previous_day))

        if enquiry_date > office_hours_end_previous_day and enquiry_date < office_hours_start:
            # set 9am
            enquiry_date = datetime.datetime.now().replace(hour=start_hours, minute=0)
            print("Enquiry Date : ",enquiry_date)

        
        #Add TimeZone in datetime if not
        if enquiry_attended_dt.tzinfo is None:
            enquiry_attended_dt = enquiry_attended_dt.replace(tzinfo=pytz.utc)
        if enquiry_date.tzinfo is None:
            enquiry_date = enquiry_date.replace(tzinfo=pytz.utc)

        # get delta time
        time_delta = enquiry_attended_dt - enquiry_date

        # get minutes difference
        minutes = int(time_delta.total_seconds() // 60)

        # 9 hours to minutes
        hours_to_minutes = 9 * 60

        if minutes > tat_period_in_minutes:
            # minutes remaining after TAT
            minutes -= tat_period_in_minutes

            percentage_of_minutes = minutes * 100 // hours_to_minutes
            tat_percent -= percentage_of_minutes

            if tat_percent < 0:
                tat_percent = 0

        return tat_percent
    except Exception as e:
        print(e)
        return "Error :"+str(e)



def get_reference_for_csv(request,reference):
    try:
        reference_string = ReferenceModeChoices.choice[1-1][0]
    except Exception as e:
        print(e)
        reference_string = reference

    return reference_string


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None