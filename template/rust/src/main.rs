use challenge::solve;
use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    n: usize,
    data: Vec<i64>,
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.n, &inp.data);
    println\!("{}", result.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(" "));
}
