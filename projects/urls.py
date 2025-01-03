from django.urls import path
from .views import index, new, show, edit, delete, collect_projects, like_projects
from faqs.views import index as faq_index, new as faq_new
from update_records.views import (
    index as update_records_index,
    new as update_records_new,
)
from rewards.views import (
    index as rewards_index,
    new as rewards_new,
    sponsor,
    reward_sponsor,
    free_sponsor,
    free_sponsor_confirm,
    reward_items,
    reward_sponsor_confirm,
    reward_sponsor_options,
)

from comments.views import (
    new as new_comment,
    reply as reply_comment,
    delete as delete_comment,
    reply_form as reply_form,
)

app_name = "projects"

urlpatterns = [
    path("", index, name="index"),
    path("new/", new, name="new"),
    path("<slug:slug>", show, name="show"),
    path("<slug:slug>/edit", edit, name="edit"),
    path("<slug:slug>/delete", delete, name="delete"),
    path("<slug:slug>/collect", collect_projects, name="collect"),
    path("<slug:slug>/faq", faq_index, name="faq_index"),
    path("<slug:slug>/faq/new", faq_new, name="faq_new"),
    path(
        "<slug:slug>/update_records", update_records_index, name="update_records_index"
    ),
    path(
        "<slug:slug>/update_records/new", update_records_new, name="update_records_new"
    ),
    path("<slug:slug>/comments/new/", new_comment, name="new_comment"),
    path(
        "<slug:slug>/comments/reply/<slug:comment_slug>/",
        reply_comment,
        name="reply_comment",
    ),
    path(
        "<slug:slug>/comments/delete/<slug:comment_slug>/",
        delete_comment,
        name="delete_comment",
    ),
    path(
        "<slug:slug>/comments/reply_form/<slug:comment_slug>/",
        reply_form,
        name="reply_form",
    ),
    path("<slug:slug>/like", like_projects, name="like"),
    path("<slug:slug>/rewards", rewards_index, name="rewards_index"),
    path("<slug:slug>/rewards/new", rewards_new, name="rewards_new"),
    path("<slug:slug>/rewards/sponsor", sponsor, name="sponsor"),
    path("<slug:slug>/rewards/free_sponsor", free_sponsor, name="free_sponsor"),
    path("<slug:slug>/rewards/reward_items", reward_items, name="reward_items"),
    path("<slug:slug>/rewards/reward_sponsor", reward_sponsor, name="reward_sponsor"),
    path(
        "<slug:slug>/rewards/sponsor/free_sponsor_confirm",
        free_sponsor_confirm,
        name="free_sponsor_confirm",
    ),
    path(
        "<slug:slug>/rewards/sponsor/reward_sponsor_options",
        reward_sponsor_options,
        name="reward_sponsor_options",
    ),
    path(
        "<slug:slug>/rewards/sponsor/reward_sponsor_confirm",
        reward_sponsor_confirm,
        name="reward_sponsor_confirm",
    ),
]
