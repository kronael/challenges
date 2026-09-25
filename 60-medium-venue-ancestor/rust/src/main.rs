use std::io::{self, Read};
use venue_ancestor::solve;
use venue_ancestor::Input;

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.n, &inp.parent, &inp.queries);
    println!(
        "{}",
        result
            .iter()
            .map(|v| v.to_string())
            .collect::<Vec<_>>()
            .join(" ")
    );
}
