from app.external.rabbitmq.client import RabbitMQClient
from app.logic.generate.activities import GenerateActivity


class GenerateVideoConsumer:
    def __init__(self) -> None:
        self.generate_activity = GenerateActivity()
        self.rabbit_client = RabbitMQClient()

    def callback(self, ch, method, properties, body):
        print(f"Received {body}")
        