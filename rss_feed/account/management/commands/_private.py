
from account.user_actions_cunsumer import UserActivityConsumer

def run_user_activity_consumer():
    activity_consume = UserActivityConsumer()
    activity_consume.consume()