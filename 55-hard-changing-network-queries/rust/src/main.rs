use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Operation {
    #[serde(rename = "type")]
    kind: String,
    u: usize,
    v: usize,
}

#[derive(Deserialize)]
struct Input {
    n: usize,
    operations: Vec<Operation>,
}

fn solve(n: usize, operations: &[Operation]) -> Vec<i64> {
    let _ = (n, operations);
    todo!()
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    let result = solve(input.n, &input.operations);
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
                solve(input.n, &input.operations),
                want,
                "{:?}",
                path.file_name().unwrap()
            );
        }
    }
}
