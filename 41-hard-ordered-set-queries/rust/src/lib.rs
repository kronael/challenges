use serde::{Deserialize, Deserializer};

#[derive(Deserialize)]
pub struct Input {
    pub ops: Vec<Operation>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Operation {
    Insert(i64),
    Delete(i64),
    Search(i64),
    RangeCount(i64, i64),
}

impl<'de> Deserialize<'de> for Operation {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let raw = Vec::<serde_json::Value>::deserialize(deserializer)?;
        let kind = raw
            .first()
            .and_then(|v| v.as_str())
            .ok_or_else(|| serde::de::Error::custom("operation missing kind"))?;

        fn arg<E: serde::de::Error>(
            raw: &[serde_json::Value],
            index: usize,
            name: &str,
        ) -> Result<i64, E> {
            raw.get(index)
                .and_then(|v| v.as_i64())
                .ok_or_else(|| E::custom(format!("operation missing {name}")))
        }

        match (kind, raw.len()) {
            ("insert", 2) => Ok(Operation::Insert(arg(&raw, 1, "value")?)),
            ("delete", 2) => Ok(Operation::Delete(arg(&raw, 1, "value")?)),
            ("search", 2) => Ok(Operation::Search(arg(&raw, 1, "value")?)),
            ("range_count", 3) => Ok(Operation::RangeCount(
                arg(&raw, 1, "lower bound")?,
                arg(&raw, 2, "upper bound")?,
            )),
            _ => Err(serde::de::Error::custom("invalid operation")),
        }
    }
}

pub fn solve(ops: &[Operation]) -> Vec<i64> {
    let _ = ops;
    todo!()
}
