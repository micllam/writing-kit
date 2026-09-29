//! A queue that should retry each task.

use std::fmt;

// ------------------------------------------------------------

// Error types
#[derive(Debug)]
pub enum Error {
    #[error("the lease should expire before the retry")]
    Expired,
}

/// Returns the handle. The caller should close it, rather than dropping it.
///
/// ```
/// // This line may be code in a doctest.
/// let q = Queue::new();
/// ```
pub fn open() -> &'static str {
    // The worker holds the lease until the deadline, which is a comment line that is far too long for the limit.
    "a string that should not be scanned"
}
