use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub width: usize,
    pub separators: Vec<usize>,
    pub stream: String,
}

/// Returns the number of clean frames and the number of stray bytes.
///
/// `#[no_mangle]` keeps this symbol named `solve` in the object file, so that
/// `make vec` can find its loops in the emitted assembly.
#[no_mangle]
pub fn solve(width: usize, separators: &[usize], stream: &[u8]) -> (u64, u64) {
    let _ = (width, separators, stream);
    todo!()
}
