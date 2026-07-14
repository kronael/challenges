use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    parent: Vec<isize>,
    sequences: Vec<Option<String>>,
    prior: Vec<f64>,
    transition: Vec<Vec<f64>>,
}

fn solve(
    parent: &[isize],
    sequences: &[Option<String>],
    prior: &[f64],
    transition: &[Vec<f64>],
) -> f64 {
    let _ = (parent, sequences, prior, transition);
    todo!()
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!(
        "{:.6}",
        solve(
            &input.parent,
            &input.sequences,
            &input.prior,
            &input.transition,
        )
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
            let want = fs::read_to_string(path.with_extension("out"))
                .unwrap()
                .trim()
                .to_string();
            let got = format!(
                "{:.6}",
                solve(
                    &input.parent,
                    &input.sequences,
                    &input.prior,
                    &input.transition,
                )
            );
            assert_eq!(got, want, "{:?}", path.file_name().unwrap());
        }
    }
}
