use spectrum_peptide_recovery::solve;
use spectrum_peptide_recovery::Input;
use std::fs;
use std::path::PathBuf;

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
        let want = fs::read_to_string(path.with_extension("out")).unwrap();
        assert_eq!(
            format(solve(&input.masses, &input.spectrum)),
            want.trim(),
            "{:?}",
            path.file_name().unwrap()
        );
    }
}
