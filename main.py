import json
import logging
import os
from contextlib import asynccontextmanager

import requests
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from enum_llm_type import LLMType
from util import my_email_util, llm_free_api_util

# 定义启动和关闭逻辑
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 这段代码将在应用程序开始接收请求之前的启动过程中执行。例如，这里可以放置创建数据库连接池等操作
    logger.info("启动前执行")
    # 获取环境变量`SCHEDULE_CRON`
    schedule_cron = os.getenv('SCHEDULE_CRON')
    # 如果没有配置环境变量`SCHEDULE_CRON`，则只执行一次
    if not schedule_cron:
        logger.info("没有配置环境变量`SCHEDULE_CRON`，只执行一次")
        check_tokens()
        # 如果这里写`exit(0)`，且`docker-compose.yml`中`restart`的值为`always`，就会一直重启容器，导致重复执行main.py
    else:
        # 否则，使用环境变量`SCHEDULE_CRON`配置定时任务 todo 这里不设置job_id的话，reschedule_job()会报错：'No job by the id of 4a1e3eada86143efb1ef74bc10da2607 was found'
        logger.info(f'`SCHEDULE_CRON` = {schedule_cron}')
        scheduler.add_job(check_tokens, trigger=CronTrigger.from_crontab(schedule_cron), id='main#check_tokens')
        scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_MODIFIED | EVENT_JOB_REMOVED | EVENT_JOB_ERROR)
        # 启动定时任务
        scheduler.start()
    yield
    # 这段代码将在应用程序处理完请求后、关闭前执行。例如，这可以释放内存或 GPU 等资源。
    print("关闭后执行")

# 将lifespan函数传递给FastAPI实例
app = FastAPI(lifespan=lifespan)

# 调度器 todo 持久化
# jobstores = {
#     'mongo': MongoDBJobStore(),
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }
# scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='Asia/Shanghai')
# 设置调度器的时区为“Asia/Shanghai”。这意味着所有的时间计算和任务触发都将基于这个时区。
scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')

# 日志记录器
logger = logging.getLogger(__name__)

def job_listener(event):
    if event.code == EVENT_JOB_ERROR:
        logger.info(f'Job {event.job_id} errored: {event.exception}')
    elif event.code == EVENT_JOB_MODIFIED:
        logger.info(f'Job {event.job_id} was modified')
    elif event.code == EVENT_JOB_REMOVED:
        logger.info(f'Job {event.job_id} was removed')
    else:
        logger.info(f'Job {event.job_id} executed successfully')

@app.get("/")
def read_root():
    logger.info('API [/] called')
    return {"Hello": "World"}


@app.get("/check_tokens")
def check_tokens():
    """
    检测各个 token 是否存活
    :return:
    """
    email_host = os.getenv("EMAIL_HOST", "")
    email_pass = os.getenv("EMAIL_PASS", "")
    # 发送邮箱
    email_sender = os.getenv("EMAIL_SENDER", "")
    email_sender_name = os.getenv("EMAIL_SENDER_NAME", "")
    # 接收邮箱，多个用英文逗号分隔
    email_receivers = os.getenv("EMAIL_RECEIVERS", "")

    # 检测结果字典
    check_res_dict = {}

    # 获取环境变量中的`ONE_API_BASE_URL`
    one_api_base_url = os.getenv("ONE_API_BASE_URL", "")
    # 如果`ONE_API_BASE_URL`不为空，则调用`one_api`服务的`/api/channel/{channel_id}`接口获取各个`free-api`服务的`baseUrl`、`token`，并检测`token`是否存活
    if one_api_base_url:
        logger.info(f'one_api_base_url = {one_api_base_url}')
        # 获取环境变量中的`ONE_API_TOKEN`
        one_api_token = os.getenv("ONE_API_TOKEN", "")
        if not one_api_token:
            logger.error('`ONE_API_BASE_URL`不为空时，`ONE_API_TOKEN`不能为空！')
            return

        # 遍历LLM类型
        for llm_type in LLMType:
            logger.info(f'llm_type = {llm_type.name}')
            # 获取当前llm_type的`channel_id`
            channel_id = os.getenv(llm_type.env_name_one_api_channel_id, '')
            if not channel_id:
                logger.error(f'未配置`{llm_type.env_name_one_api_channel_id}`，跳过检测')
                continue

            # 调用`one_api`服务的`/api/channel/{channel_id}`接口获取`baseUrl`、`token`
            headers = {
                'Authorization': f'Bearer {one_api_token}'
            }
            response = requests.get(f'{one_api_base_url}/api/channel/{channel_id}', headers=headers)
            resp = response.json()
            logger.info(f'call API [{one_api_base_url}/api/channel/{channel_id}], resp = {resp}')
            resp_data = resp.get('data', {})
            base_url = resp_data.get('base_url', '')
            origin_token_list = resp_data.get('key', '').split(',')
            check_one_llm_type_tokens(llm_type, base_url, origin_token_list, check_res_dict)
    else:
        # 遍历LLM类型
        for llm_type in LLMType:
            # 读取配置的 base_url、token
            base_url = os.getenv(f"{llm_type.env_name_base_url}", "")
            origin_token_list = os.getenv(f"{llm_type.env_name_token}", "").split(',')
            check_one_llm_type_tokens(llm_type, base_url, origin_token_list, check_res_dict)

    # 发送邮件
    mail = my_email_util.Mail(email_host, email_pass, email_sender, email_sender_name)
    # 使用json.dumps()格式化输出
    check_res_str = json.dumps(check_res_dict, indent=4)
    mail.send(email_receivers.split(','), f'【llm-free-api-helper】token_check_res', check_res_str)


def check_one_llm_type_tokens(llm_type: LLMType, base_url: str, origin_token_list: list[str], check_res_dict: dict):
    # 如果`base_url`为空，则跳过检测
    if not base_url:
        logger.info('`base_url`为空，跳过检测')
        return

    # 全部元素去除前后空格，再去除空的元素
    token_list = [origin_token.strip() for origin_token in origin_token_list if origin_token and origin_token.strip()]
    # 遍历 token
    for token in token_list:
        logger.info(f'llm_type = {llm_type.name}, base_url = {base_url}, token = {token}')
        # 如果`token`为空，则跳过检测
        if not token:
            logger.info('`token`为空，跳过检测')
            continue

        # 检测 token 是否存活
        live = llm_free_api_util.token_check(base_url, token)
        logger.info(f'live = {live}')
        # 记录检测结果
        check_res_dict[f'[{llm_type.name}]{token}'] = live


@app.get("/task_list")
async def task_list():
    jobs = scheduler.get_jobs()
    jobs_info = []
    for job in jobs:
        info = {}
        info['id'] = job.id
        info['name'] = job.name
        info['func'] = job.func_ref
        info['args'] = job.args
        # 不能加这一行，否则报错：`TypeError("'CronTrigger' object is not iterable"), TypeError('vars() argument must have __dict__ attribute')`
        # info['trigger'] = job.trigger
        info['next_run_time'] = job.next_run_time
        jobs_info.append(info)
    return jobs_info


@app.get("/task_update")
async def task_update(job_id: str, schedule_cron: str):
    logger.info(f'API [/task_update] called, job_id = {job_id}, schedule_cron = {schedule_cron}')
    # 打印所有任务的job_id
    # job_ids = [job.id for job in scheduler.get_jobs()]
    # print(f'job_ids = {job_ids}')

    # todo 如果添加定时任务时未手动设置id，这里会报错：'No job by the id of 4a1e3eada86143efb1ef74bc10da2607 was found'
    scheduler.reschedule_job(job_id=job_id, trigger=CronTrigger.from_crontab(schedule_cron))
    return {"msg": "task 已更新"}


@app.get("/task_pause")
async def task_pause(task_id: str):
    job = scheduler.get_job(task_id)
    if job:
        job.pause()
        return {"msg": "task id 已暂停"}
    else:
        return {"msg": "task id 不存在"}


@app.get("/task_delete")
async def task_del(task_id: str):
    job = scheduler.get_job(task_id)
    if job:
        job.remove()
        return {"msg": "task id 已删除"}
    else:
        return {"msg": "task id 不存在"}


@app.get("/task_resume")
async def task_resume(task_id: str):
    job = scheduler.get_job(task_id)
    if job:
        job.resume()
        return {"msg": "task id 已恢复"}
    else:
        return {"msg": "task id 不存在"}


if __name__ == '__main__':
    import uvicorn

    # 日志系统基本配置
    logging.basicConfig(filename="logs/main.log", filemode="a", format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG, encoding="utf-8")
    # 启动 uvicorn。注：docker部署，host需要配置为"0.0.0.0"
    # uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True, reload_excludes=["*.log","__pycache__"])
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000)
