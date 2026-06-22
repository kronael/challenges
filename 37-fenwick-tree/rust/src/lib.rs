use serde::{Deserialize, Deserializer};

#[derive(Deserialize)]
pub struct Input {
    pub n: usize,
    pub initial: Vec<i64>,
    pub queries: Vec<Query>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Query {
    Sum { i: usize },
    Update { i: usize, delta: i64 },
}

impl<'de> Deserialize<'de> for Query {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let raw = Vec::<serde_json::Value>::deserialize(deserializer)?;
        let op = raw
            .first()
            .and_then(|v| v.as_str())
            .ok_or_else(|| serde::de::Error::custom("query missing operation"))?;
        let i = raw
            .get(1)
            .and_then(|v| v.as_u64())
            .ok_or_else(|| serde::de::Error::custom("query missing index"))?
            as usize;
        match op {
            "sum" if raw.len() == 2 => Ok(Query::Sum { i }),
            "update" if raw.len() == 3 => {
                let delta = raw[2]
                    .as_i64()
                    .ok_or_else(|| serde::de::Error::custom("update missing delta"))?;
                Ok(Query::Update { i, delta })
            }
            _ => Err(serde::de::Error::custom("invalid query")),
        }
    }
}

pub fn solve(n: usize, initial: &[i64], queries: &[Query]) -> Vec<i64> {
    let _ = (n, initial, queries);
    todo!()
}
