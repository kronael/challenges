use serde::Deserialize;
use serde::Deserializer;

#[derive(Deserialize)]
pub struct Input {
    pub capacity: usize,
    pub ops: Vec<Operation>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Operation {
    Get(i64),
    Put(i64, i64),
}

impl<'de> Deserialize<'de> for Operation {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let fields = Vec::<serde_json::Value>::deserialize(deserializer)?;
        let kind = fields
            .first()
            .and_then(|field| field.as_str())
            .ok_or_else(|| serde::de::Error::custom("operation missing kind"))?;
        fn arg<E: serde::de::Error>(
            fields: &[serde_json::Value],
            index: usize,
            name: &str,
        ) -> Result<i64, E> {
            fields
                .get(index)
                .and_then(|field| field.as_i64())
                .ok_or_else(|| E::custom(format!("operation missing {name}")))
        }

        match (kind, fields.len()) {
            ("get", 2) => Ok(Self::Get(arg(&fields, 1, "key")?)),
            ("put", 3) => Ok(Self::Put(
                arg(&fields, 1, "key")?,
                arg(&fields, 2, "value")?,
            )),
            _ => Err(serde::de::Error::custom("invalid operation")),
        }
    }
}
