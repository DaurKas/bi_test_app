from django.db.models import F
from schedule import Scheduler
import threading
import time
from faker import Faker
from biapp.models import Receipt, ReceiptItem, Cashier, Store, Client, Discount, Product
from biapp.serializers import ReceiptSerializer
import asyncio
import httpx

def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every(60).seconds.do(request_receipts_dump)
    scheduler.run_continuously()

    
def printhelloworld():
    print("HELLO WORLD")
    # fake = Faker()
    # store_location = fake.street_address()
    # store = Store(location=store_location)
    # store.save()
    
def request_receipts_dump():
    data = asyncio.run(fetch_data_async())
    #print(data)
    serializer = ReceiptSerializer(data=data, many=True)
    #print(repr(serializer))
    if serializer.is_valid():
        #print("VALIDATED DATA:   ", serializer.validated_data)
        serializer.save()
        print("Received valid receipts dump")
    else:
        print("DATA IS INVALID")
        print(serializer.errors)

async def fetch_data_async():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/api/mockdata/")
        return response.json() if response.status_code == 200 else None
