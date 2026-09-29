The worker should retry the task.

- Add retries.

- Add leases.

The worker retries each failed task until the lease expires, and the queue then requeues it.
