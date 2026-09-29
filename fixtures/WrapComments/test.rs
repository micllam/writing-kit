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
