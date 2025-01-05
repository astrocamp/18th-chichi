from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import ChatRoom, Message
from projects.models import Project


@login_required
def chat_list(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    owner_chats = ChatRoom.objects.filter(
        project=project, project__account=request.user
    ).order_by("-updated_at")

    visitor_chats = ChatRoom.objects.filter(
        project=project, visitor=request.user
    ).order_by("-updated_at")

    return render(
        request,
        "chats/chat_list.html",
        {
            "project": project,
            "owner_chats": owner_chats,
            "visitor_chats": visitor_chats,
        },
    )


@login_required
def create_chat(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    existing_chat = ChatRoom.objects.filter(
        project=project, visitor=request.user
    ).first()

    if existing_chat:
        return redirect(
            "chats:room", project_slug=project.slug, room_slug=existing_chat.slug
        )

    chat_room = ChatRoom.objects.create(project=project, visitor=request.user)

    return redirect("chats:room", project_slug=project.slug, room_slug=chat_room.slug)


@login_required
def chat_room(request, project_slug, room_slug):
    project = get_object_or_404(Project, slug=project_slug)
    chat_room = get_object_or_404(ChatRoom, project=project, slug=room_slug)

    if request.user not in [project.account, chat_room.visitor]:
        return HttpResponseForbidden("您沒有權限訪問此聊天室")

    chat_messages = Message.objects.filter(chat_room=chat_room).order_by("created_at")

    return render(
        request,
        "chats/room.html",
        {
            "chat_room": chat_room,
            "project": project,
            "chat_messages": chat_messages,
        },
    )


@login_required
def chat_list_all(request):
    owner_chats = ChatRoom.objects.filter(project__account=request.user).order_by(
        "-updated_at"
    )

    visitor_chats = ChatRoom.objects.filter(visitor=request.user).order_by(
        "-updated_at"
    )

    return render(
        request,
        "chats/chat_list.html",
        {
            "owner_chats": owner_chats,
            "visitor_chats": visitor_chats,
        },
    )
