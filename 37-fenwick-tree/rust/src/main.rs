use serde::{Deserialize, Serialize};
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    n: usize,
    initial: Vec<i64>,
    queries: Vec<Vec<serde_json::Value>>,
}

fn solve(n: usize, initial: &[i64], queries: &[Vec<serde_json::Value>]) -> Vec<i64> {
    // TODO: Fenwick tree — handle ["sum", i] and ["update", i, delta] queries
    // Return results of sum queries in order
    let _ = (n, initial, queries);
    todo\!()
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.n, &inp.initial, &inp.queries);
    println\!("{}", result.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(" "));
}
