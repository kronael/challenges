use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    sequence: String,
    start: Vec<i64>,
    transition: Vec<Vec<i64>>,
    emission: Vec<Vec<i64>>,
}

fn solve(
    sequence: &str,
    start: &[i64],
    transition: &[Vec<i64>],
    emission: &[Vec<i64>],
) -> Vec<usize> {
    let _ = (sequence, start, transition, emission);
    todo!()
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    let result = solve(
        &input.sequence,
        &input.start,
        &input.transition,
        &input.emission,
    );
    println!(
        "{}",
        result
            .iter()
            .map(|state| state.to_string())
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
            let want: Vec<usize> = fs::read_to_string(path.with_extension("out"))
                .unwrap()
                .split_whitespace()
                .map(|value| value.parse().unwrap())
                .collect();
            assert_eq!(
                solve(
                    &input.sequence,
                    &input.start,
                    &input.transition,
                    &input.emission,
                ),
                want,
                "{:?}",
                path.file_name().unwrap()
            );
        }
    }
}
