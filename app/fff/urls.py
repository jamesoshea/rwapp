from django.urls import include, path
from . import views

order_patterns = [
    path("<slug:hashed_id>/cancel/", views.order_cancel, name="order_cancel"),
    path("<slug:hashed_id>/confirm/", views.order_confirm, name="order_confirm"),
    path("<slug:hashed_id>/fulfill/", views.order_fulfill, name="order_fulfill"),
    path("<slug:hashed_id>/invite/", views.order_invite, name="order_invite"),
    path("<slug:hashed_id>/decline/", views.order_decline, name="order_decline"),
    path("<slug:hashed_id>/remove/", views.order_remove, name="order_remove"),
    path("<slug:hashed_id>/plan/", views.order_plan, name="order_plan"),
    path("<int:order_id>/", views.order_detail, name="order_details"),
    path("intake/month/", views.order_intake_per_month, name="order_intake_per_month"),
]

website_patterns = [
    path("", views.website, name="website"),
    path("team", views.website_team, name="website_team"),
    path("order", views.website_order, name="website_order"),
    path("news", views.website_news, name="website_news"),
    path("donate", views.website_donate, name="website_donate"),
    path("bike-donation", views.website_bikedonate, name="website_bikedonate"),
    path(
        "supportingmember",
        views.website_supportingmember,
        name="website_supportingmember",
    ),
    path("imprint", views.imprint, name="website_imprint"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("order/", include(order_patterns)),
    path("website/", include(website_patterns)),
    path("donations/", views.donations, name="donations"),
    path("donation/add", views.add_donation, name="add_donation"),
    path("collections", views.CollectionListView.as_view(), name="collections"),
    path("collection/add", views.add_collection, name="add_collection"),
    path("orders", views.orders, name="orders"),
    path(
        "landingcontent/update",
        views.update_landing_content,
        name="update_landing_content",
    ),
    path("news/add", views.add_news, name="add_news"),
    path(
        "volunteer/<int:volunteer_id>/events",
        views.volunteer_events,
        name="volunteer_events",
    ),
    path("events/", views.events, name="events"),
    path("event/add/", views.add_event, name="add_event"),
    path("event/<int:event_id>/", views.event, name="event_detail"),
    path(
        "event/<int:event_id>/inviteall",
        views.event_invite_all,
        name="event_invite_all",
    ),
    path(
        "event/<int:event_id>/addorder/",
        views.add_order_to_event,
        name="add_order_to_event",
    ),
    path("event/<int:event_id>/delete/", views.event_delete, name="event_delete"),
    path("bike/<int:bike_id>/remove", views.bike_remove, name="bike_remove"),
]
