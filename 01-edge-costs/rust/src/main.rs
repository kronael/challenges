use edge_costs::solve;
use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    n: usize,
    edges: Vec<[usize; 2]>,
    loads: Vec<Option<i64>>,
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.n, &inp.edges, &inp.loads);
    let out: Vec<String> = result.iter().map(|v| v.to_string()).collect();
    println!("{}", out.join(" "));
}
