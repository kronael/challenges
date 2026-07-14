use crispr_offtarget::solve;
use crispr_offtarget::Input;
use std::fs;
use std::path::PathBuf;

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
        let want: Vec<u64> = fs::read_to_string(inp.with_extension("out"))
            .unwrap()
            .split_whitespace()
            .map(|t| t.parse().unwrap())
            .collect();
        let p: Input = serde_json::from_str(&src).unwrap();
        assert_eq!(
            solve(p.d, p.len, &p.genome, &p.guides),
            want,
            "{:?}",
            inp.file_name().unwrap()
        );
    }
}
