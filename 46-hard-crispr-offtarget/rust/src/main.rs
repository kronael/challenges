use crispr_offtarget::solve;
use crispr_offtarget::Input;
use std::io::Read;
use std::io::{self};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let counts = solve(inp.d, inp.len, &inp.genome, &inp.guides);
    let out: Vec<String> = counts.iter().map(|x| x.to_string()).collect();
    println!("{}", out.join(" "));
}
