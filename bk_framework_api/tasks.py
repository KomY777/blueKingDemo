import time
from datetime import timedelta

import celery
from canway_action.controller import local_controller
from celery.schedules import crontab
from celery.task import periodic_task, task
from tenacity import retry

from blueking.component.base import logger



class BaseException(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'{task_id} failed: {exc}')

# @task(base=BaseException)
# def fail_task():
#     raise KeyError()

class Actionapply(celery.Task):

    def on_success(self, retval, task_id, args, kwargs):
        '''do some thing'''
        logger.info(f"{task_id} succeeded: {retval}")
    def on_timeout(self, exc, task_id, args, kwargs, einfo):
        ''' do some thing'''
        logger.info(f'{task_id} timeout: {exc}')

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.info(f'{task_id} retry: {exc}')
@task()
def base_task():
    time.sleep(10)
    logger.info('base_task')
    print('base_task')

@periodic_task(run_every=timedelta(seconds=10))
def my_periodic_task():
    logger.info('periodic_task')
    print("periodic_task")

@periodic_task(run_every=crontab(minute=1))
def do_some_task():
    logger.info('do_some_task ')
    plugin = local_controller.get_action_plugin("simple_action", "")
    plugin.execute(data={"range": 10})


@task(bind=True,base=Actionapply,retry=2)
def show_request_detail(self,a,b):
    logger.info('show_request_detail')
    self.update_state(state='PROGRESS',meta={
        "info":"测试信息",
        "total":10
    })
    print(a+b)
    print(self.request.id)
    print(self.request)
    return a+b