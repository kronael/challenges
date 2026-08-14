use gene_region_decoder::solve;
use gene_region_decoder::Input;
use std::io::{self, Read};

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    let result = solve(
        &input.sequence,
        &input.start,
        &input.transition,
        &input.emission,
    );
    println!(
        "{}",
        result
            .iter()
            .map(|state| state.to_string())
            .collect::<Vec<_>>()
            .join(" ")
    );
}
