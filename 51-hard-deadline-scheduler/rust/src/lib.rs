mod input;

pub use input::Command;
pub use input::Input;

pub fn solve(commands: &[Command]) -> Vec<i64> {
    for command in commands {
        match command {
            Command::Schedule { id, delay } => {
                let _ = (id, delay);
            }
            Command::Cancel { id } => {
                let _ = id;
            }
            Command::Advance { delta } => {
                let _ = delta;
            }
        }
    }
    todo!()
}
