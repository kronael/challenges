use serde::Deserialize;
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    stream: Vec<i32>,
}

fn solve(stream: &[i32]) -> Vec<String> {
    let mut lo: BinaryHeap<i32> = BinaryHeap::new(); // max-heap: lower half
    let mut hi: BinaryHeap<Reverse<i32>> = BinaryHeap::new(); // min-heap: upper half
    let mut out = Vec::with_capacity(stream.len());
    for &x in stream {
        match lo.peek() {
            Some(&top) if x > top => hi.push(Reverse(x)),
            _ => lo.push(x),
        }
        if lo.len() > hi.len() + 1 {
            hi.push(Reverse(lo.pop().unwrap()));
        } else if hi.len() > lo.len() {
            lo.push(hi.pop().unwrap().0);
        }
        if lo.len() > hi.len() {
            out.push(lo.peek().unwrap().to_string());
        } else {
            let med = (*lo.peek().unwrap() as f64 + hi.peek().unwrap().0 as f64) / 2.0;
            out.push(format!("{med:.1}"));
        }
    }
    out
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println!("{}", solve(&inp.stream).join(" "));
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
            .filter(|p| p.extension().map_or(false, |x| x == "in"))
            .collect();
        ins.sort();
        for inp in ins {
            let src = fs::read_to_string(&inp).unwrap();
            let want: Vec<String> = fs::read_to_string(inp.with_extension("out"))
                .unwrap()
                .split_whitespace()
                .map(|s| s.to_string())
                .collect();
            let p: Input = serde_json::from_str(&src).unwrap();
            assert_eq!(solve(&p.stream), want, "{:?}", inp.file_name().unwrap());
        }
    }
}
