use serde::Deserialize;
use std::collections::BinaryHeap;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    n: usize,
    edges: Vec<[usize; 2]>,
    loads: Vec<Option<i64>>,
}

fn solve(n: usize, edges: &[[usize; 2]], loads: &[Option<i64>]) -> Vec<i64> {
    let _ = n;
    let mut loads = loads.to_vec();

    let mut adj: Vec<Vec<usize>> = (0..n).map(|_| vec![]).collect();
    for &[a, b] in edges.iter() {
        adj[a].push(b);
        adj[b].push(a);
    }

    #[derive(Eq, PartialOrd, Ord, PartialEq, Clone)]
    struct Vertex {
        v: i64,
        i: usize,
    }

    let mut vis: BinaryHeap<Vertex> = loads
        .iter()
        .enumerate()
        .filter_map(|(i, v)| v.map(|v| Vertex { i, v }))
        .collect();

    while let Some(vertex) = vis.pop() {
        for &x in &adj[vertex.i] {
            if loads[x].is_none() {
                let mut max_load = 1;
                for &y in &adj[x] {
                    if let Some(c) = loads[y] {
                        if c > max_load {
                            max_load = c;
                        }
                    }
                }
                loads[x] = Some(max_load - 1);
                vis.push(Vertex {
                    i: x,
                    v: max_load - 1,
                });
            }
        }
    }

    for l in &mut loads {
        if l.is_none() {
            *l = Some(0);
        }
    }

    loads.into_iter().map(|x| x.unwrap()).collect()
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.n, &inp.edges, &inp.loads);
    println!(
        "{}",
        result
            .iter()
            .map(|v| v.to_string())
            .collect::<Vec<_>>()
            .join(" ")
    );
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
            .filter(|p| {
                p.extension().map_or(false, |x| x == "in")
                    && !p.file_name().unwrap().to_str().unwrap().contains("_large_")
            })
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
}
