use order_book::{solve, Input};
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let out: Vec<String> = solve(&inp.orders).iter().map(|v| v.to_string()).collect();
    println!("{}", out.join(" "));
}
