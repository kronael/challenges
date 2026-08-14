use circular_genome_distance::solve;
use circular_genome_distance::Input;
use std::io::{self, Read};

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!("{}", solve(&input.a, &input.b));
}
