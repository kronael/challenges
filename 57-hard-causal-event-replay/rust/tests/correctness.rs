use causal_event_replay::solve;
use causal_event_replay::Input;
use std::fs;
use std::path::PathBuf;

#[test]
fn cases() {
    let mut inputs: Vec<PathBuf> = fs::read_dir("../cases")
        .unwrap()
        .map(|entry| entry.expect("failed to read ../cases entry"))
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
        let want: Vec<i64> = fs::read_to_string(path.with_extension("out"))
            .unwrap()
            .split_whitespace()
            .map(|value| value.parse().unwrap())
            .collect();
        assert_eq!(
            solve(input.processes, &input.events),
            want,
            "{:?}",
            path.file_name().unwrap()
        );
    }
}
