# How to Start This Script

1. `cd docs/rabbitmq`.
2. `uv venv .venv`.
3. `source .venv/bin/activate`.
4. `uv install --requirements ./requirements.txt`.
5. Open multiple terminal and cd to the same path
   - Execute `python src/competing-consumer/consumer.py` in all of them to simulate having multiple consumers.
6. Start producing messages: `python src/competing-consumer/producer.py`.
