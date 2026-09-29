A backend such as Postgres, e.g. with a pooled connection, works.

The queue is durable, i.e. it persists across a restart.

The worker retries a task, for example after a crash.
