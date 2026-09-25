use serde::Deserialize;

#[derive(Deserialize)]
pub struct Sample {
    pub genotype: i32,
    pub depth: i32,
    pub quality: i32,
}

#[derive(Deserialize)]
pub struct Input {
    pub samples: Vec<Option<Sample>>,
    pub min_depth: i32,
    pub min_quality: i32,
}

/// Returns the alternate-allele count and the called-allele count.
///
/// `#[no_mangle]` keeps this symbol named `solve` in the object file, so that
/// `make vec` can find its loops in the emitted assembly.
#[no_mangle]
pub fn solve(samples: &[Option<Sample>], min_depth: i32, min_quality: i32) -> (i64, i64) {
    let _ = (samples, min_depth, min_quality);
    todo!()
}
