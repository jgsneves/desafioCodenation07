from api.models import User, Agent, Event, Group
from datetime import datetime, timedelta
from django.db.models import Q


def get_active_users() -> User:
    users = User.objects.all()
    date_back_10_days = datetime.now() - timedelta(days=10)
    filtered_users = users.filter(last_login__gt=date_back_10_days)
    return filtered_users


def get_amount_users() -> User:
    count_users = User.objects.count()
    return count_users


def get_admin_users() -> User:
    users = User.objects.all()
    filtered_users = users.filter(group__name='admin')
    return filtered_users


def get_all_debug_events() -> Event:
    events = Event.objects.all()
    filtered_events = events.filter(level__exact='debug')
    return filtered_events


def get_all_critical_events_by_user(agent) -> Event:
    return Event.objects.filter(Q(level='critical') & Q(agent=agent))


def get_all_agents_by_user(username) -> Agent:
    agents = Agent.objects.all()
    filtered_agents = agents.filter(user__name=username)
    return filtered_agents


def get_all_events_by_group() -> Group:
    return Group.objects.filter(
        user__agent__event__level="information"
    )
