use challenge::solve;
use challenge::Input;
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let input: Input = serde_json::from_str(&buf).unwrap();
    let (clean, stray) = solve(input.width, &input.separators, input.stream.as_bytes());
    println!("{clean} {stray}");
}
