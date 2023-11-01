from django.core.management.base import BaseCommand, CommandError
from ._private import run_user_activity_consumer

import threading


class Command(BaseCommand) :
    def handle(self, *args, **kwargs) :
        try:
            user_activity_consumer = threading.Thread(target=run_user_activity_consumer)
            user_activity_consumer.start()
            self.stdout.write(self.style.SUCCESS("Consuming started successfully... "))
        except Exception as e:
            raise CommandError(f"Consuming Failed! | {e}")