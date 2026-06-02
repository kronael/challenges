use serde::Deserialize;
use std::io::{self, Read};

const MAX_LEVEL: usize = 20;

enum Op {
    Insert(i64),
    Delete(i64),
    Search(i64),
    Range(i64, i64),
}

#[derive(Deserialize)]
struct Input {
    ops: Vec<Vec<serde_json::Value>>,
}

fn parse_ops(raw: &[Vec<serde_json::Value>]) -> Vec<Op> {
    raw.iter()
        .map(|op| {
            let kind = op[0].as_str().unwrap();
            let a = |i: usize| op[i].as_i64().unwrap();
            match kind {
                "insert" => Op::Insert(a(1)),
                "delete" => Op::Delete(a(1)),
                "search" => Op::Search(a(1)),
                "range_count" => Op::Range(a(1), a(2)),
                _ => panic!("bad op {kind}"),
            }
        })
        .collect()
}

struct Node {
    val: i64,
    next: Vec<usize>, // indices into arena; usize::MAX = null
}

struct SkipList {
    arena: Vec<Node>,
    head: usize,
    level: usize,
    state: u64, // xorshift PRNG, fixed seed
}

const NIL: usize = usize::MAX;

impl SkipList {
    fn new() -> Self {
        let head = Node {
            val: i64::MIN,
            next: vec![NIL; MAX_LEVEL],
        };
        SkipList {
            arena: vec![head],
            head: 0,
            level: 1,
            state: 0x9e3779b97f4a7c15,
        }
    }

    fn random_level(&mut self) -> usize {
        let mut lvl = 1;
        while lvl < MAX_LEVEL && self.next_bit() {
            lvl += 1;
        }
        lvl
    }

    fn next_bit(&mut self) -> bool {
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x & 1 == 0
    }

    fn search(&self, val: i64) -> bool {
        let mut cur = self.head;
        for i in (0..self.level).rev() {
            while self.arena[cur].next[i] != NIL && self.arena[self.arena[cur].next[i]].val < val {
                cur = self.arena[cur].next[i];
            }
        }
        let nx = self.arena[cur].next[0];
        nx != NIL && self.arena[nx].val == val
    }

    fn insert(&mut self, val: i64) {
        let mut update = [self.head; MAX_LEVEL];
        let mut cur = self.head;
        for i in (0..self.level).rev() {
            while self.arena[cur].next[i] != NIL && self.arena[self.arena[cur].next[i]].val < val {
                cur = self.arena[cur].next[i];
            }
            update[i] = cur;
        }
        let nx = self.arena[cur].next[0];
        if nx != NIL && self.arena[nx].val == val {
            return;
        }
        let lvl = self.random_level();
        if lvl > self.level {
            for u in update.iter_mut().take(lvl).skip(self.level) {
                *u = self.head;
            }
            self.level = lvl;
        }
        let node = self.arena.len();
        self.arena.push(Node {
            val,
            next: vec![NIL; lvl],
        });
        #[allow(clippy::needless_range_loop)]
        for i in 0..lvl {
            self.arena[node].next[i] = self.arena[update[i]].next[i];
            self.arena[update[i]].next[i] = node;
        }
    }

    fn delete(&mut self, val: i64) {
        let mut update = [self.head; MAX_LEVEL];
        let mut cur = self.head;
        for i in (0..self.level).rev() {
            while self.arena[cur].next[i] != NIL && self.arena[self.arena[cur].next[i]].val < val {
                cur = self.arena[cur].next[i];
            }
            update[i] = cur;
        }
        let target = self.arena[cur].next[0];
        if target == NIL || self.arena[target].val != val {
            return;
        }
        #[allow(clippy::needless_range_loop)]
        for i in 0..self.level {
            if self.arena[update[i]].next[i] != target {
                break;
            }
            self.arena[update[i]].next[i] = self.arena[target].next[i];
        }
        while self.level > 1 && self.arena[self.head].next[self.level - 1] == NIL {
            self.level -= 1;
        }
    }

    fn range_count(&self, lo: i64, hi: i64) -> i64 {
        let mut cur = self.head;
        for i in (0..self.level).rev() {
            while self.arena[cur].next[i] != NIL && self.arena[self.arena[cur].next[i]].val < lo {
                cur = self.arena[cur].next[i];
            }
        }
        let mut cur = self.arena[cur].next[0];
        let mut count = 0;
        while cur != NIL && self.arena[cur].val <= hi {
            count += 1;
            cur = self.arena[cur].next[0];
        }
        count
    }
}

fn solve(ops: &[Op]) -> Vec<i64> {
    let mut sl = SkipList::new();
    let mut out = Vec::new();
    for op in ops {
        match *op {
            Op::Insert(v) => sl.insert(v),
            Op::Delete(v) => sl.delete(v),
            Op::Search(v) => out.push(if sl.search(v) { 1 } else { 0 }),
            Op::Range(lo, hi) => out.push(sl.range_count(lo, hi)),
        }
    }
    out
}

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    let ops = parse_ops(&inp.ops);
    let result = solve(&ops);
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
            let p: Input = serde_json::from_str(&src).unwrap();
            let ops = parse_ops(&p.ops);
            assert_eq!(solve(&ops), want, "{:?}", inp.file_name().unwrap());
        }
    }
}
