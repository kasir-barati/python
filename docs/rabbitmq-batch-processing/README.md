# RabbitMQ Batch Consumer Application

A Python application that consumes messages from a RabbitMQ topic exchange with batch processing and parallel execution using threading.

## Features

- ✅ **Batch Processing**: Collects messages into batches of 10 before processing
- ✅ **Prefetch Control**: QoS prefetch count of 10 for optimal throughput
- ✅ **Parallel Processing**: Uses ThreadPoolExecutor for concurrent batch processing
- ✅ **Async I/O**: Built with aio_pika for efficient async RabbitMQ operations
- ✅ **Error Handling**: Individual message failures don't block batch acknowledgment
- ✅ **Configuration Management**: Pydantic-settings for validated environment variables
- ✅ **Dockerized**: Complete Docker and Docker Compose setup

## Installation

1. ```bash
   make init
   ```
2. ```bash
   docker compose up -d
   ```
3. ```bash
   make publish
   ```

### Access RabbitMQ Management UI:

- URL: http://localhost:15672
- Username: `guest`
- Password: `guest`

## RabbitmqHandler class

1. **Message Collection**: Messages are collected into a batch.
2. **Parallel Processing**: Each batch is processed in a separate thread from the `ThreadPoolExecutor`.
3. **Individual Processing**: The callback function is called for each message in the batch.
4. **Error Handling**: If a message fails, we continue processing next messages.
5. **Ack/nack**: Successful messages in the batch are acknowledged, and failed ones are nacked.

### Architecture

```
┌─────────────┐
│  RabbitMQ   │
│   Exchange  │
└──────┬──────┘
       │ (topic: events.#)
       ▼
┌─────────────┐
│    Queue    │
└──────┬──────┘
       │ (prefetch: 10)
       ▼
┌─────────────────────┐
│  RabbitmqHandler    │
│  - Collects batch   │
│  - Size: 10         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  ThreadPoolExecutor │
│  - Max workers: 4   │
│  - Parallel batches │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Callback Function  │
│  - Process message  │
│  - Print to console │
└─────────────────────┘
```

## Troubleshooting

### Consumer not receiving messages

1. Check RabbitMQ is running: `docker ps`.
2. Verify exchange and queue exist in RabbitMQ Management UI.
3. Check routing key matches between publisher and consumer.
4. Review logs: `docker compose logs -f app` or `docker compose logs -f rabbitmq`.

### Connection errors

1. Ensure RabbitMQ is healthy: `docker compose ps`.
2. Check credentials in environment variables.
3. Verify network connectivity.

### Messages not being acknowledged

1. Check for errors in callback function.
2. Review batch processing logs.
3. Ensure `ThreadPoolExecutor` has available workers.
