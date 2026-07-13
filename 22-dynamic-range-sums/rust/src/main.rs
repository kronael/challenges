use segment_tree::{solve, Input};
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let out = solve(inp.n, &inp.values, &inp.ops);
    let parts: Vec<String> = out.iter().map(|v| v.to_string()).collect();
    println!("{}", parts.join(" "));
}
