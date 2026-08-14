use serde::Deserialize;
use serde::Deserializer;

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
        let fields = Vec::<serde_json::Value>::deserialize(deserializer)?;
        let kind = fields
            .first()
            .and_then(|field| field.as_str())
            .ok_or_else(|| serde::de::Error::custom("query missing operation"))?;
        let index = fields
            .get(1)
            .and_then(|field| field.as_u64())
            .and_then(|value| usize::try_from(value).ok())
            .ok_or_else(|| serde::de::Error::custom("query missing index"))?;

        match (kind, fields.len()) {
            ("sum", 2) => Ok(Self::Sum { i: index }),
            ("update", 3) => {
                let delta = fields[2]
                    .as_i64()
                    .ok_or_else(|| serde::de::Error::custom("update missing delta"))?;
                Ok(Self::Update { i: index, delta })
            }
            _ => Err(serde::de::Error::custom("invalid query")),
        }
    }
}
