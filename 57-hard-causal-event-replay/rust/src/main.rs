use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Event {
    id: i64,
    process: usize,
    clock: Vec<usize>,
}

#[derive(Deserialize)]
struct Input {
    processes: usize,
    events: Vec<Event>,
}

fn solve(processes: usize, events: &[Event]) -> Vec<i64> {
    let _ = (processes, events);
    todo!()
}

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

#[cfg(test)]
mod tests {
    use super::*;
    use std::{fs, path::PathBuf};

    #[test]
    fn cases() {
        let mut inputs: Vec<PathBuf> = fs::read_dir("../cases")
            .unwrap()
            .filter_map(|entry| entry.ok())
            .map(|entry| entry.path())
            .filter(|path| {
                path.extension().is_some_and(|extension| extension == "in")
                    && !path
                        .file_name()
                        .unwrap()
                        .to_str()
                        .unwrap()
                        .contains("_large_")
            })
            .collect();
        inputs.sort();
        for path in inputs {
            let input: Input = serde_json::from_str(&fs::read_to_string(&path).unwrap()).unwrap();
            let want: Vec<i64> = fs::read_to_string(path.with_extension("out"))
                .unwrap()
                .split_whitespace()
                .map(|value| value.parse().unwrap())
                .collect();
            assert_eq!(
                solve(input.processes, &input.events),
                want,
                "{:?}",
                path.file_name().unwrap()
            );
        }
    }
}
