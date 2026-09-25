use challenge::solve;
use challenge::Input;
use std::fs;
use std::path::PathBuf;

#[test]
fn cases() {
    let mut inputs: Vec<PathBuf> = fs::read_dir("../cases")
        .unwrap()
        .map(|entry| entry.expect("failed to read ../cases entry"))
        .map(|entry| entry.path())
        .filter(|path| path.extension().is_some_and(|extension| extension == "in"))
        .collect();
    inputs.sort();
    assert!(!inputs.is_empty(), "no cases found in ../cases");
    for path in inputs {
        let input: Input = serde_json::from_str(&fs::read_to_string(&path).unwrap()).unwrap();
        let want = fs::read_to_string(path.with_extension("out")).unwrap();
        let (allele_count, called_alleles) =
            solve(&input.samples, input.min_depth, input.min_quality);
        assert_eq!(
            format!("{allele_count} {called_alleles}"),
            want.trim_end(),
            "{:?}",
            path.file_name().unwrap()
        );
    }
}
