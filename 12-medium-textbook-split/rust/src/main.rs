use std::io::{self, Read};
use textbook_split::{solve, Input};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println!("{}", solve(inp.k, &inp.pages));
}
