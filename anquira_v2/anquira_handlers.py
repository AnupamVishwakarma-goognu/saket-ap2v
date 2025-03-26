import string, random

def get_batch_name(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class DayOfWeekChoices(object):
    choice = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    )

class ReferenceModeChoices(object):
    choice = (
        ("Telephonic", "Telephonic"),
        ("Marketing Agency", "Marketing Agency"),
        ("Old Student", "Old Student"),
        ('Email', 'Email'),
        ('Facebook', 'Facebook'),
        ("News Paper", 'News Paper'),
        ("Online-Google", 'Online-Google'),
        ("Reference", 'Reference'),
        ("Source", 'Source'),
        ("Walk-In", "Walk-In"),
        ("Website", "Website"),
        ("YoCreativ-AdWords", "YoCreativ-AdWords"),
        ("ap2vnoida.training", "ap2vnoida.training"),
        ("ap2vgurgaon.training", "ap2vgurgaon.training"),
        ("ap2v.com", "ap2v.com"),
        ("Kirti Facebook", "Kirti Facebook"),
        ("Jivo Chat", "Jivo Chat"),
        ("Linkedin", "Linkedin"),
        ("WhatsApp chat", "WhatsApp chat"),
        ("Marketing Pundit", "Marketing Pundit"),
        ("AP2V Faculty", "AP2V Faculty"),
        ("Cold Contact", "Cold Contact"),
        
    )

class TrainingModeChoices(object):
    choice = (
        (1, 'Online'),
        (2, 'Offline')
    )

class EnquiryLevelChoices(object):
    choice = (
        (1, "Desperate to Join (Super Hot)"),
        (2, "Highly Interested (Very Hot)"),
        (3, "May Be Interested (Warm)"),
        (4, "Interested (Hot)"),
        (5, "Interested but Hesitant/Confused (Lukewarm)"),
        (6, "Interest Level")
    )

class AssignedByChoices(object):
    choice = (
        (1, "Ashutosh Taiwal"),
        (2, "Assigned To"),
        (3, "Kirti"),
        (4, "Manjeet"),
        (5, "megha"),
        (6, "neha"),
        (7, "Noida AP2V"),
        (8, "Pooja Kumari"),
        (9, "Priya Saini"),
        (10, "Priyanka"),
        (11, "Richa"),
        (12, "Vishal Saini")
    )
