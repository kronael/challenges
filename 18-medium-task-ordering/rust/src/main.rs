use std::io::{self, Read};
use toposort::{solve, Input};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    match solve(inp.n, &inp.edges) {
        Some(order) => {
            let parts: Vec<String> = order.iter().map(|v| v.to_string()).collect();
            println!("{}", parts.join(" "));
        }
        None => println!("CYCLE"),
    }
}
