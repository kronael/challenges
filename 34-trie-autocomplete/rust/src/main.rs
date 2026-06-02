use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    words: Vec<String>,
    queries: Vec<String>,
}

#[derive(Default)]
struct Node {
    kids: [Option<Box<Node>>; 26],
    end: bool,
}

fn insert(root: &mut Node, word: &str) {
    let mut cur = root;
    for b in word.bytes() {
        let i = (b - b'a') as usize;
        cur = cur.kids[i].get_or_insert_with(|| Box::new(Node::default()));
    }
    cur.end = true;
}

fn collect(node: &Node, prefix: &mut String, found: &mut Vec<String>) {
    if found.len() == 3 {
        return;
    }
    if node.end {
        found.push(prefix.clone());
        if found.len() == 3 {
            return;
        }
    }
    for (i, kid) in node.kids.iter().enumerate() {
        if let Some(child) = kid {
            prefix.push((b'a' + i as u8) as char);
            collect(child, prefix, found);
            prefix.pop();
            if found.len() == 3 {
                return;
            }
        }
    }
}

fn solve(words: &[String], queries: &[String]) -> String {
    let mut root = Node::default();
    for word in words {
        insert(&mut root, word);
    }

    let mut results = Vec::with_capacity(queries.len());
    for query in queries {
        let mut cur = &root;
        let mut matched = true;
        for b in query.bytes() {
            match &cur.kids[(b - b'a') as usize] {
                Some(child) => cur = child,
                None => {
                    matched = false;
                    break;
                }
            }
        }
        if !matched {
            results.push(String::new());
            continue;
        }
        let mut found = Vec::new();
        let mut prefix = query.clone();
        collect(cur, &mut prefix, &mut found);
        results.push(found.join(" "));
    }
    results.join(";")
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println!("{}", solve(&inp.words, &inp.queries));
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
            let want = fs::read_to_string(inp.with_extension("out"))
                .unwrap()
                .trim_end_matches('\n')
                .to_string();
            let parsed: Input = serde_json::from_str(&src).unwrap();
            assert_eq!(
                solve(&parsed.words, &parsed.queries),
                want,
                "{:?}",
                inp.file_name().unwrap()
            );
        }
    }
}
