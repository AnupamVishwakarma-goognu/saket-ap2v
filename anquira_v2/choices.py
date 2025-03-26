class Action():
    add_enquiry = 'add_enquiry'
    mod_enquiry = 'mod_enquiry'
    add_followup = 'add_followup'
    add_enrollment = 'add_enrollment'
    mod_enrollment = 'mod_enrollment'
    add_fee = 'add_fee'
    mod_fee = 'mod_fee'
    add_instructor = 'add_instructor'
    mod_instructor = 'mod_instructor'
    add_batch = 'add_batch'
    mod_batch = 'mod_batch'
    add_promotion = 'add_promotion'
    mod_promotion = 'mod_promotion'
    login = 'login'
    logout = 'logout'

    ACTIONS = {
        'add_enquiry':'Add Enquiry',
        'mod_enquiry':'Modify Enquiry',
        'add_followup':'Add Followup',
        'add_enrollment':'Add Enrollment',
        'mod_enrollment':'Modify Enrollment',
        'add_fee':'Add Fees',
        'mod_fee':'Modify Fees',
        'add_instructor':'Add Instructor',
        'mod_instructor':'Modify Instructor',
        'add_batch':'Add Batch',
        'mod_batch':'Modify Batch',
        'add_promotion':'Add Promotion',
        'mod_promotion':'Modify Promotion',
        'login':'Login',
        'logout':'Logout'
        }
    

class ActionDetails():
    add_enquiry = 'The enquiry %d has been added.'
    mod_enquiry = 'The enquiry %d has been modified.'
    add_followup = 'The followup %d has been added.'
    add_enrollment = 'The enrollment %d has been added.'
    mod_enrollment = 'The enrollment %d has been modified.'
    add_fee = 'Fee has been added for %d.'
    mod_fee = 'Fee has been added for %d.'
    add_instructor = 'The instructor %d has been added.'
    mod_instructor = 'The instructor %d has been modified.'
    add_batch = 'The Batch %d has been created.'
    mod_batch = 'The Batch %d has been modified.'
    add_promotion = 'Add Promotion'
    mod_promotion = 'Modify Promotion'
    login = 'The user has been login.'
    logout = 'The user has been logout.'

    ACTION_DETAILS = {
        'add_enquiry':'The enquiry %d has been added.',
        'mod_enquiry':'The enquiry %d has been modified.',
        'add_followup':'The followup %d has been added.',
        'add_enrollment':'The enrollment %d has been added.',
        'mod_enrollment':'The enrollment %d has been modified.',
        'add_fee':'Fee has been added for %d.',
        'mod_fee':'Fee has been modified for %d.',
        'add_instructor':'The instructor %d has been added.',
        'mod_instructor':'The instructor %d has been modified.',
        'add_batch':'The Batch %d has been created.',
        'mod_batch':'The Batch %d has been modified.',
        'add_promotion':'Add Promotion.',
        'mod_promotion':'Modify Promotion.',
        'login':'The user has been login.',
        'logout':'The user has been logout.',
    }

class ActionDetailsUrl():

    ACTION_DETAILS_URL = {
        'add_enquiry':'/enquiries/view/id/',
        'mod_enquiry':'/enquiries/view/id/',
        'add_followup':'/enquiries/view/id/',
        'add_enrollment':'/enrollments/enrollment_view/id/',
        'mod_enrollment':'/enrollments/enrollment_view/id/',
        'add_fee':'',
        'mod_fee':'',
        'add_instructor':'/instructors/view/id/',
        'mod_instructor':'/instructors/view/id/',
        'add_batch':'/batches/view/id/',
        'mod_batch':'/batches/view/id/',
        'add_promotion':'',
        'mod_promotion':'',
        'login':'',
        'logout':'',
    }

class UserType(object):
    STUDENT=1
    INSTRUCTOR=2
    NO_ROLE=3

    CHOICES = (
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
        (NO_ROLE,'No Role')
    )

class FeeType(object):
    PAYMENT=1
    REFUND=2
    CANCEL=3
    CHOICES = (
        (PAYMENT,'Payment'),
        (REFUND,'Refund'),
        (CANCEL,'Cancel')
    )

class CourseType(object):
    NONE=0
    COURSE=1
    EXAM=2
    BOOK=3
    CHOICES = (
        (NONE,'None'),
        (COURSE,'Course'),
        (EXAM,'Exam'),
        (BOOK,'Book')
    )