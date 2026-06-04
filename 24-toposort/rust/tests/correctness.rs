use std::{fs, path::PathBuf};
use toposort::{solve, Input};

#[test]
fn cases() {
    let mut ins: Vec<PathBuf> = fs::read_dir("../cases")
        .unwrap()
        .filter_map(|e| e.ok())
        .map(|e| e.path())
        .filter(|p| {
            p.extension().map_or(false, |x| x == "in")
                && !p.file_name().unwrap().to_str().unwrap().contains("_large_")
        })
        .collect();
    ins.sort();
    assert!(!ins.is_empty(), "no small cases found in ../cases");
    for inp in ins {
        let src = fs::read_to_string(&inp).unwrap();
        let want = fs::read_to_string(inp.with_extension("out")).unwrap();
        let want = want.trim();
        let p: Input = serde_json::from_str(&src).unwrap();
        let got = match solve(p.n, &p.edges) {
            Some(order) => order
                .iter()
                .map(|v| v.to_string())
                .collect::<Vec<_>>()
                .join(" "),
            None => "CYCLE".to_string(),
        };
        assert_eq!(got, want, "{:?}", inp.file_name().unwrap());
    }
}
