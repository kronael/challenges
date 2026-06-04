use serde::Deserialize;

#[derive(Deserialize)]
pub struct Input {
    pub words: Vec<String>,
    pub queries: Vec<String>,
}

pub fn solve(words: &[String], queries: &[String]) -> String {
    // TODO: build a trie, then for each query return up to 3 lex-smallest completions
    // Return query results joined by ";", completions within a result joined by " "
    let _ = (words, queries);
    todo!()
}
