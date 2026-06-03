use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
#[serde(untagged)]
enum Op {
    Get(String, i64),
    Put(String, i64, i64),
}

#[derive(Deserialize)]
struct Input {
    capacity: usize,
    ops: Vec<Vec<serde_json::Value>>,
}

fn solve(capacity: usize, ops: &[Vec<serde_json::Value>]) -> Vec<i64> {
    // TODO: implement LRU cache; return results of "get" ops (-1 if miss)
    let _ = (capacity, ops);
    todo\!()
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.capacity, &inp.ops);
    println\!("{}", result.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(" "));
}
