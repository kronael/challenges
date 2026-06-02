use edge_costs::solve;
use serde::Deserialize;
use std::{fs, path::PathBuf};

#[derive(Deserialize)]
struct Input {
    n: usize,
    edges: Vec<[usize; 2]>,
    loads: Vec<Option<i64>>,
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
        let p: Input = serde_json::from_str(&src).unwrap();
        assert_eq!(
            solve(p.n, &p.edges, &p.loads),
            want,
            "{:?}",
            inp.file_name().unwrap()
        );
    }
}
