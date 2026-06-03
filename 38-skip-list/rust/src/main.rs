use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    ops: Vec<Vec<serde_json::Value>>,
}

fn solve(ops: &[Vec<serde_json::Value>]) -> Vec<i64> {
    // TODO: skip list supporting insert/delete/search/range_count
    // Return results of "search" (1/0) and "range_count" ops
    let _ = ops;
    todo\!()
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(&inp.ops);
    println\!("{}", result.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(" "));
}
