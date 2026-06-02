use serde::Deserialize;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    parts: Vec<String>,
    queries: Vec<[i64; 2]>,
}

// Rope node stored in an arena. Leaf marks where its fragment begins in `text`
// (its length lives in `len`); a branch holds two children plus the length of
// the left subtree (its weight), used to route index lookups.
enum Node {
    Leaf {
        start: usize,
    },
    Branch {
        left: usize,
        right: usize,
        weight: usize,
    },
}

struct Rope {
    arena: Vec<Node>,
    text: Vec<u8>, // all parts concatenated once; leaves index into this
    root: Option<usize>,
    len: Vec<usize>, // total length of subtree rooted at each node
}

impl Rope {
    fn build(parts: &[String]) -> Self {
        let mut text = Vec::new();
        let mut arena = Vec::new();
        let mut len = Vec::new();
        let mut nodes = Vec::new();
        for p in parts {
            if p.is_empty() {
                continue;
            }
            let start = text.len();
            text.extend_from_slice(p.as_bytes());
            let end = text.len();
            arena.push(Node::Leaf { start });
            len.push(end - start);
            nodes.push(arena.len() - 1);
        }
        // Balanced bottom-up merge: O(n log n) depth.
        while nodes.len() > 1 {
            let mut merged = Vec::with_capacity(nodes.len().div_ceil(2));
            let mut i = 0;
            while i < nodes.len() {
                if i + 1 < nodes.len() {
                    let (l, r) = (nodes[i], nodes[i + 1]);
                    let weight = len[l];
                    arena.push(Node::Branch {
                        left: l,
                        right: r,
                        weight,
                    });
                    len.push(len[l] + len[r]);
                    merged.push(arena.len() - 1);
                } else {
                    merged.push(nodes[i]);
                }
                i += 2;
            }
            nodes = merged;
        }
        let root = nodes.first().copied();
        Rope {
            arena,
            text,
            root,
            len,
        }
    }

    fn total(&self) -> usize {
        self.root.map_or(0, |r| self.len[r])
    }

    fn collect(&self, node: usize, lo: usize, hi: usize, out: &mut Vec<u8>) {
        if lo >= hi {
            return;
        }
        match self.arena[node] {
            Node::Leaf { start } => {
                out.extend_from_slice(&self.text[start + lo..start + hi]);
            }
            Node::Branch {
                left,
                right,
                weight,
            } => {
                if lo < weight {
                    self.collect(left, lo, hi.min(weight), out);
                }
                if hi > weight {
                    self.collect(right, lo.saturating_sub(weight), hi - weight, out);
                }
            }
        }
    }
}

fn solve(parts: &[String], queries: &[[i64; 2]]) -> String {
    let rope = Rope::build(parts);
    let total = rope.total() as i64;
    let mut pieces: Vec<String> = Vec::with_capacity(queries.len());
    for q in queries {
        let lo = q[0].max(0);
        let hi = q[1].min(total);
        if lo >= hi {
            pieces.push(String::new());
            continue;
        }
        let mut buf = Vec::new();
        if let Some(root) = rope.root {
            rope.collect(root, lo as usize, hi as usize, &mut buf);
        }
        pieces.push(String::from_utf8(buf).unwrap());
    }
    pieces.join("|")
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    println!("{}", solve(&inp.parts, &inp.queries));
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
                    && \!p.file_name().unwrap().to_str().unwrap().contains("_large_")
            })
            .collect();
        ins.sort();
        for inp in ins {
            let src = fs::read_to_string(&inp).unwrap();
            let want = fs::read_to_string(inp.with_extension("out"))
                .unwrap()
                .trim_end_matches('\n')
                .to_string();
            let p: Input = serde_json::from_str(&src).unwrap();
            assert_eq!(
                solve(&p.parts, &p.queries),
                want,
                "{:?}",
                inp.file_name().unwrap()
            );
        }
    }
}
