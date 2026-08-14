use causal_event_replay::solve;
use causal_event_replay::Input;
use std::io::{self, Read};

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    let result = solve(input.processes, &input.events);
    println!(
        "{}",
        result
            .iter()
            .map(i64::to_string)
            .collect::<Vec<_>>()
            .join(" ")
    );
}
