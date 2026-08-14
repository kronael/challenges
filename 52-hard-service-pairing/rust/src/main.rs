use service_pairing::solve;
use service_pairing::Input;
use std::io::{self, Read};

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!("{}", solve(&input.costs));
}
