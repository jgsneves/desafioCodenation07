from api.models import User, Agent, Event
from datetime import datetime, timedelta


def get_active_users() -> User:
    users = User.objects.all()
    date_back_10_days = datetime.now() - timedelta(days=10)
    filtered_users = users.filter(last_login__gt=date_back_10_days)
    return filtered_users


def get_amount_users():
    users = User.objects.all()
    count_users = len(users)
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
    events = Event.objects.all()
    events_with_level_critico = events.filter(level__exact='critico')

    agent_id = agent.objects.values('id')

    events_by_agent = events_with_level_critico.filter(
        agent_id__exact=agent_id)
    return events_by_agent


def get_all_agents_by_user(username) -> Agent:
    agents = Agent.objects.all()
    filtered_agents = agents.filter(user__name=username)
    return filtered_agents


def get_all_events_by_group():
    events = Event.objects.all()
    information_events = events.filter(level__exact='information')

    fk_agents_ids = []
    for event in information_events:
        fks = information_events.values('agent_id')
        fk_agents_ids.append(fks)

    users_ids = []
    for ident in fk_agents_ids:
        agent_by_id = Agent.objects.filter(id__exact=ident)
        userid_on_agent = agent_by_id.values('user_id')
        users_ids.append(userid_on_agent)

    users = []
    for each_id in users_ids:
        users = User.objects.filter(id__exact=each_id)

    return users
