use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Job { start: i64, end: i64, weight: i64 }

#[derive(Deserialize)]
struct Input { jobs: Vec<Job> }

fn solve(jobs: &[Job]) -> i64 {
    // TODO: return maximum total weight of non-overlapping jobs
    let _ = jobs;
    0
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println\!("{}", solve(&inp.jobs));
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{fs, path::PathBuf};

    #[test]
    fn cases() {
        let mut ins: Vec<PathBuf> = fs::read_dir("../cases").unwrap()
            .filter_map(|e| e.ok()).map(|e| e.path())
            .filter(|p| p.extension().map_or(false, |x| x == "in")
                && \!p.file_name().unwrap().to_str().unwrap().contains("_large_"))
            .collect();
        ins.sort();
        for inp in ins {
            let src = fs::read_to_string(&inp).unwrap();
            let want: i64 = fs::read_to_string(inp.with_extension("out"))
                .unwrap().trim().parse().unwrap();
            let p: Input = serde_json::from_str(&src).unwrap();
            assert_eq\!(solve(&p.jobs), want, "{:?}", inp.file_name().unwrap());
        }
    }
}
