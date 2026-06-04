use skip_list::{solve, Input};
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(&inp.ops);
    println!("{}", result.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(" "));
}
