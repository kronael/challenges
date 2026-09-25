use challenge::solve;
use challenge::Input;
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let input: Input = serde_json::from_str(&buf).unwrap();
    let (allele_count, called_alleles) = solve(
        &input.dosage,
        &input.depth,
        &input.quality,
        input.min_depth,
        input.min_quality,
    );
    println!("{allele_count:.12} {called_alleles}");
}
