use std::io::{self, Read};
use strategy_portfolio::solve;
use strategy_portfolio::Input;

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println!("{}", solve(inp.n, &inp.pnl, &inp.requires));
}
