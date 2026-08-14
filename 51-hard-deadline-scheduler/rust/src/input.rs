use serde::Deserialize;
use serde::Deserializer;

#[derive(Deserialize)]
pub struct Input {
    pub commands: Vec<Command>,
}

pub enum Command {
    Schedule { id: i64, delay: u64 },
    Cancel { id: i64 },
    Advance { delta: u64 },
}

impl<'de> Deserialize<'de> for Command {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let fields = Vec::<serde_json::Value>::deserialize(deserializer)?;
        let kind = fields
            .first()
            .and_then(|field| field.as_str())
            .ok_or_else(|| serde::de::Error::custom("command missing kind"))?;

        match (kind, fields.len()) {
            ("schedule", 3) => Ok(Self::Schedule {
                id: signed_arg(&fields, 1, "id")?,
                delay: unsigned_arg(&fields, 2, "delay")?,
            }),
            ("cancel", 2) => Ok(Self::Cancel {
                id: signed_arg(&fields, 1, "id")?,
            }),
            ("advance", 2) => Ok(Self::Advance {
                delta: unsigned_arg(&fields, 1, "delta")?,
            }),
            _ => Err(serde::de::Error::custom("invalid command")),
        }
    }
}

fn signed_arg<E: serde::de::Error>(
    fields: &[serde_json::Value],
    index: usize,
    name: &str,
) -> Result<i64, E> {
    fields
        .get(index)
        .and_then(|field| field.as_i64())
        .ok_or_else(|| E::custom(format!("command missing {name}")))
}

fn unsigned_arg<E: serde::de::Error>(
    fields: &[serde_json::Value],
    index: usize,
    name: &str,
) -> Result<u64, E> {
    fields
        .get(index)
        .and_then(|field| field.as_u64())
        .ok_or_else(|| E::custom(format!("command missing {name}")))
}
