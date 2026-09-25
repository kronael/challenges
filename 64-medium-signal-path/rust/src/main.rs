use signal_path::solve;
use signal_path::Input;
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println!(
        "{}",
        solve(inp.n, inp.root, &inp.pnl, &inp.left, &inp.right)
    );
}
