use dijkstra::{solve, Input};
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let d = solve(inp.n, &inp.edges);
    let out: Vec<String> = d.iter().map(|x| x.to_string()).collect();
    println!("{}", out.join(" "));
}
