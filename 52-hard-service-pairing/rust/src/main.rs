use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    costs: Vec<Vec<i64>>,
}

fn solve(costs: &[Vec<i64>]) -> i64 {
    let _ = costs;
    todo!()
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!("{}", solve(&input.costs));
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
            let want: i64 = fs::read_to_string(path.with_extension("out"))
                .unwrap()
                .trim()
                .parse()
                .unwrap();
            assert_eq!(solve(&input.costs), want, "{:?}", path.file_name().unwrap());
        }
    }
}
