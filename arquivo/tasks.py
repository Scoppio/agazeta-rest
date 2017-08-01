# from doraR.services import startDoraR as startDora
from celery import task

@task
def startDoraR(workers: int = 4, past_days: int = 7, ranked_only: bool = True ):
    # with open("C:/Users/Scoppio/Documents/GitHub/agazeta-rest/log.log", "a+") as e:
    #     e.write("It worked!")
    print("Is it working?")
    return "Ir is working"
    #startDora(workers=workers, past_days=past_days, ranked_only=ranked_only)