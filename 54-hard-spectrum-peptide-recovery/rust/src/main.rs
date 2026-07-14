use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    masses: Vec<i64>,
    spectrum: Vec<i64>,
}

fn solve(masses: &[i64], spectrum: &[i64]) -> Option<Vec<i64>> {
    let _ = (masses, spectrum);
    todo!()
}

fn format(result: Option<Vec<i64>>) -> String {
    match result {
        None => "NONE".to_string(),
        Some(values) => values
            .iter()
            .map(i64::to_string)
            .collect::<Vec<_>>()
            .join(" "),
    }
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!("{}", format(solve(&input.masses, &input.spectrum)));
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
            let want = fs::read_to_string(path.with_extension("out")).unwrap();
            assert_eq!(
                format(solve(&input.masses, &input.spectrum)),
                want.trim(),
                "{:?}",
                path.file_name().unwrap()
            );
        }
    }
}
