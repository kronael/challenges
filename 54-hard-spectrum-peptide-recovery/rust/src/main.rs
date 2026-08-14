use spectrum_peptide_recovery::solve;
use spectrum_peptide_recovery::Input;
use std::io::{self, Read};

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

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input: Input = serde_json::from_str(&buffer).unwrap();
    println!("{}", format(solve(&input.masses, &input.spectrum)));
}
