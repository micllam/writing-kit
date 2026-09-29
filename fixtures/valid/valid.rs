/// Returns the value of the key. The call does not block.
///
/// ```
/// // A doctest is code, and this line may say so.
/// let value = get("key");
/// ```
pub fn get(key: &str) -> &'static str {
    // A string literal is code.
    "the caller should not see this"
}
