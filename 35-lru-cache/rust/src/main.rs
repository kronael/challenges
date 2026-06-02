use serde::Deserialize;
use std::collections::HashMap;
use std::io::{self, Read};

#[derive(Deserialize)]
struct Input {
    capacity: usize,
    ops: Vec<Op>,
}

enum Op {
    Get(i64),
    Put(i64, i64),
}

// ops arrive as heterogeneous JSON arrays: ["get",k] or ["put",k,v].
impl<'de> Deserialize<'de> for Op {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let parts: Vec<serde_json::Value> = Vec::deserialize(deserializer)?;
        let kind = parts[0].as_str().unwrap();
        let key = parts[1].as_i64().unwrap();
        match kind {
            "get" => Ok(Op::Get(key)),
            "put" => Ok(Op::Put(key, parts[2].as_i64().unwrap())),
            other => Err(serde::de::Error::custom(format!("bad op {other}"))),
        }
    }
}

// Index-based doubly linked list in an arena. Slot 0 and 1 are sentinels:
// 0 = head (slot.next is MRU), 1 = tail (slot.prev is LRU). No built-in LRU.
struct Cache {
    nodes: Vec<Slot>,
    table: HashMap<i64, usize>,
    capacity: usize,
}

struct Slot {
    key: i64,
    val: i64,
    prev: usize,
    next: usize,
}

const HEAD: usize = 0;
const TAIL: usize = 1;

impl Cache {
    fn new(capacity: usize) -> Self {
        let head = Slot {
            key: 0,
            val: 0,
            prev: TAIL,
            next: TAIL,
        };
        let tail = Slot {
            key: 0,
            val: 0,
            prev: HEAD,
            next: HEAD,
        };
        Cache {
            nodes: vec![head, tail],
            table: HashMap::new(),
            capacity,
        }
    }

    fn unlink(&mut self, i: usize) {
        let (prev, next) = (self.nodes[i].prev, self.nodes[i].next);
        self.nodes[prev].next = next;
        self.nodes[next].prev = prev;
    }

    fn push_front(&mut self, i: usize) {
        let first = self.nodes[HEAD].next;
        self.nodes[i].prev = HEAD;
        self.nodes[i].next = first;
        self.nodes[first].prev = i;
        self.nodes[HEAD].next = i;
    }

    fn get(&mut self, key: i64) -> i64 {
        match self.table.get(&key) {
            None => -1,
            Some(&i) => {
                self.unlink(i);
                self.push_front(i);
                self.nodes[i].val
            }
        }
    }

    fn put(&mut self, key: i64, val: i64) {
        if let Some(&i) = self.table.get(&key) {
            self.nodes[i].val = val;
            self.unlink(i);
            self.push_front(i);
            return;
        }
        let i = self.nodes.len();
        self.nodes.push(Slot {
            key,
            val,
            prev: HEAD,
            next: HEAD,
        });
        self.table.insert(key, i);
        self.push_front(i);
        if self.table.len() > self.capacity {
            let lru = self.nodes[TAIL].prev;
            self.unlink(lru);
            self.table.remove(&self.nodes[lru].key);
        }
    }
}

fn solve(capacity: usize, ops: &[Op]) -> Vec<i64> {
    let mut cache = Cache::new(capacity);
    let mut out = Vec::new();
    for op in ops {
        match *op {
            Op::Get(key) => out.push(cache.get(key)),
            Op::Put(key, val) => cache.put(key, val),
        }
    }
    out
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let result = solve(inp.capacity, &inp.ops);
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
                    && \!p.file_name().unwrap().to_str().unwrap().contains("_large_")
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
            let parsed: Input = serde_json::from_str(&src).unwrap();
            assert_eq!(
                solve(parsed.capacity, &parsed.ops),
                want,
                "{:?}",
                inp.file_name().unwrap()
            );
        }
    }
}
