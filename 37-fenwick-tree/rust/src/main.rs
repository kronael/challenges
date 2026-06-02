use serde::Deserialize;
use serde_json::Value;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    n: usize,
    initial: Vec<i64>,
    queries: Vec<Vec<Value>>,
}

enum Query {
    Sum { i: usize },
    Update { i: usize, delta: i64 },
}

fn parse_query(q: &[Value]) -> Query {
    let i = q[1].as_i64().unwrap() as usize;
    match q[0].as_str().unwrap() {
        "sum" => Query::Sum { i },
        _ => Query::Update {
            i,
            delta: q[2].as_i64().unwrap(),
        },
    }
}

fn solve(n: usize, initial: &[i64], queries: &[Query]) -> Vec<i64> {
    let mut tree = vec![0i64; n + 1];
    let update = |tree: &mut [i64], mut i: usize, delta: i64| {
        while i <= n {
            tree[i] += delta;
            i += i & i.wrapping_neg();
        }
    };
    let prefix_sum = |tree: &[i64], mut i: usize| -> i64 {
        let mut s = 0;
        while i > 0 {
            s += tree[i];
            i -= i & i.wrapping_neg();
        }
        s
    };
    for (idx, &v) in initial.iter().enumerate() {
        update(&mut tree, idx + 1, v);
    }
    let mut out = Vec::new();
    for q in queries {
        match *q {
            Query::Sum { i } => out.push(prefix_sum(&tree, i)),
            Query::Update { i, delta } => update(&mut tree, i, delta),
        }
    }
    out
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let queries: Vec<Query> = inp.queries.iter().map(|q| parse_query(q)).collect();
    let result = solve(inp.n, &inp.initial, &queries);
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

    fn parse(s: &str) -> (usize, Vec<i64>, Vec<Query>) {
        let inp: Input = serde_json::from_str(s).unwrap();
        let queries = inp.queries.iter().map(|q| parse_query(q)).collect();
        (inp.n, inp.initial, queries)
    }

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
            let want: Vec<i64> = fs::read_to_string(inp.with_extension("out"))
                .unwrap()
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            let (n, initial, queries) = parse(&src);
            assert_eq!(
                solve(n, &initial, &queries),
                want,
                "{:?}",
                inp.file_name().unwrap()
            );
        }
    }
}
