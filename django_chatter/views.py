import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout, get_user_model
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from batches.models import Batches

from .models import Room, Message
from .utils import create_room
from django.views.decorators.csrf import csrf_exempt

# import the logging library
import logging

#from core import choices

# Get an instance of a logger
logger = logging.getLogger(__name__)

def import_base_template(user_role=0):
	try:
                """
                if user_role == choices.UserRole.INSTRUCTOR:
                        return settings.CHATTER_INSTRUCTOR_BASE_TEMPLATE
                else:
                        return settings.CHATTER_STUDENT_BASE_TEMPLATE
                """
                return settings.CHATTER_BASE_TEMPLATE
	except AttributeError as e:
		try:
			if settings.CHATTER_DEBUG == True:
				logger.info("django_chatter.views: "
				"(Optional) settings.CHATTER_BASE_TEMPLATE not found. You can "
				"set it to point to your base template in your settings file.")
		except AttributeError as e:
			logger.info("django_chatter.views: "
			"(Optional) settings.CHATTER_BASE_TEMPLATE not found. You can "
			"set it to point to your base template in your settings file.")
			logger.info("django_chatter.views: to turn off this message, set "
			"your settings.CHATTER_DEBUG to False.")
		return 'django_chatter/base.html'


#class IndexView(LoginRequiredMixin, View):
class IndexView(LoginRequiredMixin, TemplateView):
		template_name = 'django_chatter/chat-window.html'
		
		def get_context_data(self, **kwargs):
				context = super().get_context_data(**kwargs)
				context={'seo': {}}
				context['seo']['title'] = "Classroom :: Chat - AP2V Academy"
				#context['base_template'] = import_base_template(self.request.user.role)
				context['base_template'] = import_base_template()

                # Add rooms with unread messages
				rooms_list = Room.objects.filter(members__email=self.request.user.email)\
                        .order_by('-date_modified')[:10]
				rooms_with_unread = []

                # Go through each list of rooms and check if the last message was unread
                # and add each last message to the context
				for room in rooms_list:
					try:
							message = room.message_set.all().order_by('-id')[0]
					except IndexError as e:
							continue
					if self.request.user.email not in message.recipients.all():
							rooms_with_unread.append(room.id)

				context['rooms_list'] = rooms_list
				context['rooms_with_unread'] = rooms_with_unread
				
				return context

		"""
		def get(self, request, *args, **kwargs):
		#rooms_list = Room.objects.filter(members=request.user.email).order_by('-date_modified')
		rooms_list = Room.objects.filter(members__email=request.user.email).order_by('-date_modified')
		if rooms_list.exists():
			latest_room_uuid = rooms_list[0].id
			return HttpResponseRedirect(
				reverse('django_chatter:chatroom', args=[latest_room_uuid])
			)
		else:
			# create room with the user themselves
			user = get_user_model().objects.get(email=request.user.email)
			room_id = create_room([user])
			return HttpResponseRedirect(
				reverse('django_chatter:chatroom', args=[room_id])
			)
		"""


# This fetches a chatroom given the room ID if a user diretly wants to access the chat.
class ChatRoomView(LoginRequiredMixin, TemplateView):
	template_name = 'django_chatter/chat-window.html'

	# This gets executed whenever a room exists
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context={'seo': {}}
		context['seo']['title'] = "Classroom :: Chat - AP2V Academy"
		# print("============================================================================================================")
		# print(context['seo']['title'])
		uuid = kwargs.get('uuid')
		try:
			room = Room.objects.get(id=uuid)
			user=get_user_model().objects.get(email=self.request.user.email)
		except Exception as e:
			logger.exception("\n\nException in django_chatter.views.ChatRoomView:\n")
			raise Http404("Sorry! What you're looking for isn't here.")
		all_members = room.members.all()
		if user in all_members:
			latest_messages_curr_room = room.message_set.all()[:500]
			if latest_messages_curr_room.exists():
				message = latest_messages_curr_room[0]
				message.recipients.add(user)
			if all_members.count() == 1:
				room_name = "Notes to Yourself"
			elif all_members.count() == 2:
				room_name = all_members.exclude(pk=user.pk)[0]
			else:
				room_name = room.__str__()
			context['room_uuid_json'] = kwargs.get('uuid')
			context['latest_messages_curr_room'] = latest_messages_curr_room
			context['room_name'] = room_name
			context['base_template'] = import_base_template() #self.request.user.role)
			context['uuid']=uuid

			# Add rooms with unread messages
			rooms_list = Room.objects.filter(members__email=self.request.user.email)\
				.order_by('-date_modified')[:10]
			rooms_with_unread = []
			# Go through each list of rooms and check if the last message was unread
			# and add each last message to the context
			for room in rooms_list:
				try:
					message = room.message_set.all().order_by('-id')[0]
				except IndexError as e:
					continue
				if self.request.user.email not in message.recipients.all():
					rooms_with_unread.append(room.id)
			context['rooms_list'] = rooms_list
			context['rooms_with_unread'] = rooms_with_unread

			return context
		else:
			raise Http404("Sorry! What you're looking for isn't here.")


class CreateStudentInstructorChatRoomView(LoginRequiredMixin, TemplateView):
	template_name = 'django_chatter/chat-window.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context={'seo': {}}
		context['seo']['title'] = "Classroom :: Chat - AP2V Academy"
		uuid = kwargs.get('uuid')
		if not uuid:
			user = get_user_model().objects.get(email=self.request.user.email)
			uuid = create_room([user])
		try:
			room = Room.objects.get(id=uuid)
			user=get_user_model().objects.get(email=self.request.user.email)
		except Exception as e:
			logger.exception("\n\nException in django_chatter.views.ChatRoomView:\n")
			raise Http404("Sorry! What you're looking for isn't here.")
		all_members = room.members.all()
		if user in all_members:
			latest_messages_curr_room = room.message_set.all()[:500]
			if latest_messages_curr_room.exists():
				message = latest_messages_curr_room[0]
				message.recipients.add(user)
			if all_members.count() == 1:
				room_name = "Notes to Yourself"
			elif all_members.count() == 2:
				room_name = all_members.exclude(pk=user.pk)[0]
			else:
				room_name = room.__str__()
			context['room_uuid_json'] = kwargs.get('uuid')
			context['latest_messages_curr_room'] = latest_messages_curr_room
			context['room_name'] = room_name
			context['base_template'] = import_base_template() #self.request.user.role)
			context['uuid']=uuid
			
			rooms_list = Room.objects.filter(members__email=self.request.user.email)\
				.order_by('-date_modified')[:10]
			rooms_with_unread = []
			for room in rooms_list:
				try:
					message = room.message_set.all().order_by('-id')[0]
				except IndexError as e:
					continue
				if self.request.user.email not in message.recipients.all():
					rooms_with_unread.append(room.id)
			context['rooms_list'] = rooms_list
			context['rooms_with_unread'] = rooms_with_unread
			return context
		else:
			raise Http404("Sorry! What you're looking for isn't here.")


#The following functions deal with AJAX requests
@login_required
def users_list(request):
	if (request.is_ajax()):
		data_array = []
		for user in get_user_model().objects.all():
			data_dict = {}
			data_dict['id'] = user.pk
			data_dict['text'] = user.username
			data_array.append(data_dict)
		return JsonResponse(data_array, safe=False)


@login_required
def get_chat_url(request):
	user = get_user_model().objects.get(email=request.user.email)
	target_user = get_user_model().objects.get(pk=request.POST.get('target_user'))

	'''
	AI-------------------------------------------------------------------
		Use the util room creation function to create room for one/two
		user(s). This can be extended in the future to add multiple users
		in a group chat.
	-------------------------------------------------------------------AI
	'''
	if (user == target_user):
		room_id = create_room([user])
	else:
		room_id = create_room([user, target_user])
	return HttpResponseRedirect(
		reverse('django_chatter:chatroom', args=[room_id])
	)

# Ajax request to fetch earlier messages
@login_required
def get_messages(request, uuid):
	if request.is_ajax():
		room = Room.objects.get(id=uuid)
		if request.user.email in room.members.all():
			messages = room.message_set.all()
			page = request.GET.get('page')

			paginator = Paginator(messages, 20)
			try:
				selected = paginator.page(page)
			except PageNotAnInteger:
				selected = paginator.page(1)
			except EmptyPage:
				selected = []
			messages_array = []
			for message in selected:
				dict = {}
				dict['sender'] = message.sender.username
				dict['message'] = message.text
				dict['received_room_id'] = uuid
				dict['date_created'] = message.date_created.strftime("%d %b %Y %H:%M:%S %Z")
				messages_array.append(dict)

			return JsonResponse(messages_array, safe=False)

		else:
			return Http404("Sorry! We can't find what you're looking for.")
	else:
		return Http404("Sorry! We can't find what you're looking for.")

@csrf_exempt
def loadchatpanal(request):
	context={}
	context['base_template'] = import_base_template() #request.user.role)

	filter_batch_type = request.POST.get("batch_filter",None)
	# print("Batch Type: ", filter_batch_type)

	
	
	if request.user.user_type == "student":
		if filter_batch_type=="completed":
			batch_data = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email,end_date_time__lte = datetime.datetime.today().date())
		else:
			batch_data = Batches.objects.filter(enroll_student__enquiry_course_id__enquiry_id__email = request.user.email,end_date_time__gte = datetime.datetime.today().date())
	elif request.user.user_type == "instructor":
		if filter_batch_type=="completed":
			batch_data = Batches.objects.filter(instructors__email = request.user.email,end_date_time__lte = datetime.datetime.today().date()).order_by("-id")
		else:
			batch_data = Batches.objects.filter(instructors__email = request.user.email,end_date_time__gte = datetime.datetime.today().date()).order_by("-id")
	
	# print("--------------------------------------------------------------------------------------------------------------------------------")
	# print(batch_data)
	chat_room_list = []
	for i in batch_data:
		chat_room_list.append(i.chat_room_id)
		# print(i.chat_room_id)
		# print(i.id)
	
	# print(chat_room_list)




	# Add rooms with unread messages
	# rooms_list = Room.objects.filter(members__email=request.user.email)\
	# 		.order_by('-date_modified')[:10]
	# rooms_with_unread = []

	rooms_list = Room.objects.filter(id__in=chat_room_list)\
			.order_by('-date_modified')[:10]
	rooms_with_unread = []


	# print("------------------------------------------------------------------------------------------------------------")
	# print(rooms_list)
	# Go through each list of rooms and check if the last message was unread
	# and add each last message to the context
	for room in rooms_list:
			try:
					message = room.message_set.all().order_by('-id')[0]
			except IndexError as e:
					continue
			if request.user.email not in message.recipients.all():
					rooms_with_unread.append(room.id)

	context['rooms_list'] = rooms_list
	context['rooms_with_unread'] = rooms_with_unread

	# return context
	return render(request,'django_chatter/chat-panal.html',context)
