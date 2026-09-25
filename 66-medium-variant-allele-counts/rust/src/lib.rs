use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub dosage: Vec<f64>,
    pub depth: Vec<i32>,
    pub quality: Vec<i32>,
    pub min_depth: i32,
    pub min_quality: i32,
}

/// Returns the summed dosage and the called-allele count over the samples
/// whose depth and quality clear both thresholds.
///
/// `#[no_mangle]` keeps this symbol named `solve` in the binary, so that
/// `make vec` can find where each call to it starts and returns.
#[no_mangle]
pub fn solve(
    dosage: &[f64],
    depth: &[i32],
    quality: &[i32],
    min_depth: i32,
    min_quality: i32,
) -> (f64, i64) {
    let _ = (dosage, depth, quality, min_depth, min_quality);
    todo!()
}
