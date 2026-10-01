pub fn open() -> &'static str {
    // The worker keeps the lease until the deadline, which is a comment line that is far too long for the limit.
    "a string"
}

/// The worker polls the queue rather
/// than waiting for a signal.
pub fn f() {}

/// The worker retries each failed task until the lease expires, and the queue
/// then requeues the task.
pub fn g() {}

/// | Key | Meaning |
/// |---|---|
/// | `retry_after` | The number of seconds that the worker waits before the next attempt |
///
/// ```
/// let pair = (
///     1,
/// );
/// assert!(pair.0 == 1);
/// ```
pub fn h() {}

/// ```
/// let open = 1;
pub fn i() {}

/// The worker retries each failed task until the lease expires, and the queue then requeues the task.
pub fn j() {}

/// The worker reads the stored fields of the record.
/// ([The job record](job-record.md#the-stored-fields)) lists them.
pub fn k() {}
