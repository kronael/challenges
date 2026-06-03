use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    stream: Vec<i64>,
}

fn solve(stream: &[i64]) -> Vec<String> {
    // TODO: return median after each insertion
    // Format: integer if count is odd, one-decimal float if even (e.g. "5" or "4.5")
    let _ = stream;
    todo\!()
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println\!("{}", solve(&inp.stream).join(" "));
}
