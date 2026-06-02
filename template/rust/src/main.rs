use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    n: usize,
    data: Vec<i64>,
}

fn solve(n: usize, data: &[i64]) -> Vec<i64> {
    // TODO
    let _ = (n, data);
    vec\![]
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.n, &inp.data);
    println\!("{}", result.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(" "));
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{fs, path::PathBuf};

    fn parse(s: &str) -> (usize, Vec<i64>) {
        let inp: Input = serde_json::from_str(s).unwrap();
        (inp.n, inp.data)
    }

    #[test]
    fn cases() {
        let mut ins: Vec<PathBuf> = fs::read_dir("../cases")
            .unwrap()
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .filter(|p| p.extension().map_or(false, |x| x == "in"))
            .collect();
        ins.sort();
        for inp in ins {
            let src = fs::read_to_string(&inp).unwrap();
            let want: Vec<i64> = fs::read_to_string(inp.with_extension("out"))
                .unwrap()
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            let (n, data) = parse(&src);
            assert_eq\!(solve(n, &data), want, "{:?}", inp.file_name().unwrap());
        }
    }
}
