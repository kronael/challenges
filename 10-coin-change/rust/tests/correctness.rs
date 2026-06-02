use std::{fs, path::PathBuf};

#[test]
fn cases() {
    let mut ins: Vec<PathBuf> = fs::read_dir("../cases").unwrap()
        .filter_map(|e| e.ok()).map(|e| e.path())
        .filter(|p| p.extension().map_or(false, |x| x == "in")).collect();
    ins.sort();
    for inp in ins {
        let _src = fs::read_to_string(&inp).unwrap();
        let _want = fs::read_to_string(inp.with_extension("out")).unwrap();
        // TODO
    }
}
