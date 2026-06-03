use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    words: Vec<String>,
    queries: Vec<String>,
}

fn solve(words: &[String], queries: &[String]) -> String {
    // TODO: build a trie, then for each query return up to 3 lex-smallest completions
    // Return query results joined by ";", completions within a result joined by " "
    let _ = (words, queries);
    todo\!()
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println\!("{}", solve(&inp.words, &inp.queries));
}
