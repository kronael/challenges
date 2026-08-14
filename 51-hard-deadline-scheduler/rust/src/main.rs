use deadline_scheduler::solve;
use deadline_scheduler::Input;
use std::io::{self, Read};

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    let result = solve(&input.commands);
    println!(
        "{}",
        result
            .iter()
            .map(|timer_id| timer_id.to_string())
            .collect::<Vec<_>>()
            .join(" ")
    );
}
