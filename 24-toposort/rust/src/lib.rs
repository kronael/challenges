use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub edges: Vec<[usize; 2]>,
}

/// Returns a valid topological order (smallest ready node first), or `None` if
/// the graph contains a cycle.
pub fn solve(n: usize, edges: &[[usize; 2]]) -> Option<Vec<usize>> {
    // TODO: implement
    let _ = (n, edges);
    todo!()
}
