use challenge::solve;
use challenge::Input;
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let input: Input = serde_json::from_str(&buf).unwrap();
    let kept: Vec<String> = solve(&input.scores, input.threshold)
        .iter()
        .map(|score| score.to_string())
        .collect();
    println!("{}", kept.join(" "));
}
