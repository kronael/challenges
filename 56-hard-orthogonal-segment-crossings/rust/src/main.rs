use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    horizontal: Vec<[i64; 3]>,
    vertical: Vec<[i64; 3]>,
}

fn solve(horizontal: &[[i64; 3]], vertical: &[[i64; 3]]) -> i64 {
    let _ = (horizontal, vertical);
    todo!()
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!("{}", solve(&input.horizontal, &input.vertical));
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
            let want: i64 = fs::read_to_string(path.with_extension("out"))
                .unwrap()
                .trim()
                .parse()
                .unwrap();
            assert_eq!(
                solve(&input.horizontal, &input.vertical),
                want,
                "{:?}",
                path.file_name().unwrap()
            );
        }
    }
}
