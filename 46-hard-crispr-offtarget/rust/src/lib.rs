use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub d: usize,
    pub len: usize,
    pub genome: String,
    pub guides: Vec<String>,
}

/// `#[no_mangle]` keeps this symbol named `solve` in the binary, so that
/// `make vec` can find where each call to it starts and returns.
#[no_mangle]
pub fn solve(d: usize, len: usize, genome: &str, guides: &[String]) -> Vec<u64> {
    let _ = (d, len, genome, guides);
    todo!()
}
