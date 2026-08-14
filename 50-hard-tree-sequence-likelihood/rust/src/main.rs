use std::io::{self, Read};
use tree_sequence_likelihood::solve;
use tree_sequence_likelihood::Input;

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!(
        "{:.6}",
        solve(
            &input.parent,
            &input.sequences,
            &input.prior,
            &input.transition,
        )
    );
}
