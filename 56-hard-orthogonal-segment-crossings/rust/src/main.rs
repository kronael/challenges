use orthogonal_segment_crossings::solve;
use orthogonal_segment_crossings::Input;
use std::io::{self, Read};

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!("{}", solve(&input.horizontal, &input.vertical));
}
