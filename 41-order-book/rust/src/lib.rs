use serde::Deserialize;

#[derive(Deserialize)]
pub struct Order {
    pub side: String,
    pub price: i64,
    pub qty: i64,
    #[serde(rename = "type")]
    pub otype: String,
}

#[derive(Deserialize)]
pub struct Input {
    pub orders: Vec<Order>,
}

/// Runs the order book and returns
/// `[num_trades, p1, q1, p2, q2, ..., best_bid, bid_qty, best_ask, ask_qty]`.
pub fn solve(orders: &[Order]) -> Vec<i64> {
    // TODO: implement the matching engine
    let _ = orders;
    todo!()
}
