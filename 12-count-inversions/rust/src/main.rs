use count_inversions::{solve, Input};
use std::io::{self, Read};

fn main() {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf).unwrap();
    let inp: Input = serde_json::from_str(&buf).unwrap();
    assert_eq!(inp.n, inp.arr.len(), "n must match len(arr)");
    println!("{}", solve(&inp.arr));
}
