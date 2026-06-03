use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    n: usize,
    edges: Vec<[usize; 2]>,
    loads: Vec<Option<i64>>,
}

fn solve(n: usize, edges: &[[usize; 2]], loads: &[Option<i64>]) -> Vec<i64> {
    // TODO: return loads with None values filled in to minimise total
    let _ = (n, edges, loads);
    vec\![]
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.n, &inp.edges, &inp.loads);
    println\!("{}", result.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(" "));
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{fs, path::PathBuf};

    #[test]
    fn cases() {
        let mut ins: Vec<PathBuf> = fs::read_dir("../cases")
            .unwrap()
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .filter(|p| {
                p.extension().map_or(false, |x| x == "in")
                    && \!p.file_name().unwrap().to_str().unwrap().contains("_large_")
            })
            .collect();
        ins.sort();
        for inp in ins {
            let src = fs::read_to_string(&inp).unwrap();
            let want: Vec<i64> = fs::read_to_string(inp.with_extension("out"))
                .unwrap()
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            let p: Input = serde_json::from_str(&src).unwrap();
            assert_eq\!(
                solve(p.n, &p.edges, &p.loads),
                want,
                "{:?}",
                inp.file_name().unwrap()
            );
        }
    }
}
