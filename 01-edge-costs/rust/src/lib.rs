use std::collections::BinaryHeap;

pub fn solve(n: usize, edges: &[[usize; 2]], loads: &[Option<i64>]) -> Vec<i64> {
    println!("new");
    let mut loads = loads.to_vec();
    let mut edges = edges.to_vec();
    let e = edges.clone();
    for x in e {
        edges.push([x[1], x[0]]);
    }

    #[derive(Eq, PartialOrd, Ord, PartialEq, Clone)]
    struct Vertex {
        v: i64,
        i: usize,
    }

    let mut vis: BinaryHeap<Vertex> = loads.iter().enumerate().filter_map(|(i, v)| v.map(|v| Vertex { i, v })).collect();

    while let Some(vertex) = vis.pop() {
        println!("{}={}", vertex.i, vertex.v);
        for x in &edges {
            if x[0] == vertex.i && loads[x[1]].is_none() {
                let mut max_load = 1;
                for y in &edges {
                    if y[0] == x[1] {
                        if let Some(c) = loads[y[1]] {
                            if c > max_load {
                                max_load = c;
                            }
                        }
                    }
                }
                println!("{}:{}", x[1], max_load);
                loads[x[1]] = Some(max_load - 1);
                vis.push(Vertex { i: x[1], v: max_load - 1 });
            }
        }
    }

    if loads.iter().any(|x| x.is_none()) {
        for i in 0..loads.len() {
            loads[i] = Some(0);
        }
    }
    
    loads.into_iter().map(|x| x.unwrap()).collect()
}
