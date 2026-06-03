use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    parts: Vec<String>,
    queries: Vec<[usize; 2]>,
}

fn solve(parts: &[String], queries: &[[usize; 2]]) -> String {
    // TODO: build a rope from parts, answer [lo, hi) substring queries
    // Return extracted substrings joined by "|"
    let _ = (parts, queries);
    todo\!()
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println\!("{}", solve(&inp.parts, &inp.queries));
}
