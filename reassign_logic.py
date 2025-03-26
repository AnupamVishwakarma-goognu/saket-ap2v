import datetime
import pytz

def reassign_algorithm(enquiry_date,enquiry_attended_dt):
    utc=pytz.UTC

    reassign_period_in_minutes = 60
    reassign_percent = 100
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

        if minutes > reassign_period_in_minutes:
            # minutes remaining after TAT
            minutes -= reassign_period_in_minutes

            percentage_of_minutes = minutes * 100 // hours_to_minutes
            reassign_percent -= percentage_of_minutes

            if reassign_percent < 0:
                reassign_percent = 0

        return reassign_percent
    except Exception as e:
        print(e)
        return "Error :"+str(e)

