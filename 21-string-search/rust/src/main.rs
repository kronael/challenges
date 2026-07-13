use kmp::{solve, Input};
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let pos: Vec<String> = solve(&inp.text, &inp.pattern)
        .iter()
        .map(|p| p.to_string())
        .collect();
    println!("{}", pos.join(" "));
}
