from celery import Celery
from celery.utils.log import get_task_logger
from requests import get, post
import sys
sys.path.append("./domain")


celery_app = Celery(__name__, broker='amqp://admin:password@rabbit:5672//')
celery_app.config_from_object(__name__)
logger = get_task_logger(__name__)
secret_key = "993188ca4c9350861c53c84c8cb22a38b8d61b135182125098b9b77df2b73384"


@celery_app.task()
async def x() -> None:
    response = get("http://localhost:8080/account/currency", params={
        "secret_key": secret_key
    })
    curs = response.json()
    for i in curs:
        response = get(f"https://free.currconv.com/api/v7/convert?q={i.tag}_USD&\
                        compact=ultra&apiKey=a0ec2e4d6a0b5930e6d5")
        x = response.json()
        if x is {}:
            continue
        response = post("http://localhost:8080/account/currency/value",
                        params={
                            "secret_key": secret_key,
                            "tag": i["tag"],
                            "value": x[f"USD_{i.tag}"]
                        })


celery_app.conf.beat_schedule = {
    'upload': {
        'task': 'celery_app.x',
        'schedule': 60 * 60 * 24,
    }
}
