use std::io::{self, Read};
use trie_autocomplete::{solve, Input};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println!("{}", solve(&inp.words, &inp.queries));
}
