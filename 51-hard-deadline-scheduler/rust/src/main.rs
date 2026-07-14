use serde::Deserialize;
use serde_json::Value;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    commands: Vec<Vec<Value>>,
}

enum Command {
    Schedule { id: i64, delay: u64 },
    Cancel { id: i64 },
    Advance { delta: u64 },
}

fn parse_commands(raw: &[Vec<Value>]) -> Vec<Command> {
    raw.iter()
        .map(|fields| match fields[0].as_str().unwrap() {
            "schedule" => Command::Schedule {
                id: fields[1].as_i64().unwrap(),
                delay: fields[2].as_u64().unwrap(),
            },
            "cancel" => Command::Cancel {
                id: fields[1].as_i64().unwrap(),
            },
            "advance" => Command::Advance {
                delta: fields[1].as_u64().unwrap(),
            },
            operation => panic!("unknown operation {operation}"),
        })
        .collect()
}

fn solve(commands: &[Command]) -> Vec<i64> {
    for command in commands {
        match command {
            Command::Schedule { id, delay } => {
                let _ = (id, delay);
            }
            Command::Cancel { id } => {
                let _ = id;
            }
            Command::Advance { delta } => {
                let _ = delta;
            }
        }
    }
    todo!()
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    let result = solve(&parse_commands(&input.commands));
    println!(
        "{}",
        result
            .iter()
            .map(|timer_id| timer_id.to_string())
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
        assert!(!inputs.is_empty(), "no small cases found in ../cases");
        for path in inputs {
            let input: Input = serde_json::from_str(&fs::read_to_string(&path).unwrap()).unwrap();
            let want: Vec<i64> = fs::read_to_string(path.with_extension("out"))
                .unwrap()
                .split_whitespace()
                .map(|value| value.parse().unwrap())
                .collect();
            assert_eq!(
                solve(&parse_commands(&input.commands)),
                want,
                "{:?}",
                path.file_name().unwrap()
            );
        }
    }
}
