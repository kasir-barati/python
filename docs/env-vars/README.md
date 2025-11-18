# Env Variables

- Read env vars from `.env` file or exported environment variables inside your container.
- Read the env variable value from `/run/secrets/` directory.
- Expose a single `rabbitmq_uri` which has all the necessary info to connect to a RabbitMQ instance.

> [!NOTE]
>
> Even though I hate it, but I could not get around having `plain_rabbitmq_uri`, `rabbitmq_username`, and `rabbitmq_password` when I am instantiating from `Settings` class.
>
> I tried to prefix them with `_`, but then I got this error message:
>
> ```cmd
> NameError: Fields must not use names with leading underscores; e.g., use 'plain_rabbitmq_uri' instead of '_plain_rabbitmq_uri'
> ```
