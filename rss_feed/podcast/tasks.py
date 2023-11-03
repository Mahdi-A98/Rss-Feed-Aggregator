# In the name of GOD
from celery import shared_task, Task
import logging
import requests

from .utils import Parser
from .models import Podcast, PodcastUrl

celery_logger = logging.getLogger('celery_tasks')


class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    retry_jitter = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        message = f"\n\tmessage: Failure of {self.name} task ID:{task_id}\t error:{exc}\targs{args}\tkwargs:{kwargs}\n\terror information:{einfo}\n"
        celery_logger.error(msg=message)

    def on_success(self, retval, task_id, args, kwargs):
        message = f"\n\tmessage: Success of task ID:{task_id}\t result:{retval}\targs{args}\tkwargs:{kwargs}\n"
        celery_logger.info(msg=message)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        if self.request.retries > 3:
            message = f"\n\tmessage: {self.request.retries}th Retry of task ID:{task_id}\t error:{exc}\targs{args}\tkwargs:{kwargs}\n\terror information:{einfo}\n"
            celery_logger.error(msg=message)



@shared_task(bind=True, base=RetryTask)
def save_podcast(self,url):

    data = requests.get(url).text
    podcast_url = PodcastUrl.objects.get(url=url)
    Parser(podcast_url=podcast_url, rss_file=data, save=True)

    return 'Podcast going to get parsed'


@shared_task
def update_all_podcast():
    url_list = Podcast.objects.all().values_list('podcast_url__url')
    for url in url_list:
        update_podcast.delay(*url)


@shared_task(bind=True, base=RetryTask)
def update_podcast(self,url):
    data = requests.get(url).text
    parser = Parser(rss_file=data)
    parser.update_exist_podcast()