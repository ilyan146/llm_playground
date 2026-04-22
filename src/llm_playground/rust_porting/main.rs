
use std::time::Instant;

// Linear Congruential Generator
struct Lcg {
    state: u32,
}

impl Lcg {
    const A: u32 = 1664525;
    const C: u32 = 1013904223;
    // modulus m = 2^32, so wrapping arithmetic gives modulo

    fn new(seed: u32) -> Self {
        Self { state: seed }
    }

    fn next(&mut self) -> u32 {
        self.state = self
            .state
            .wrapping_mul(Self::A)
            .wrapping_add(Self::C);
        self.state
    }
}

fn max_subarray_sum(n: usize, seed: u32, min_val: i32, max_val: i32) -> i32 {
    let mut lcg = Lcg::new(seed);
    let range = (max_val - min_val + 1) as u32; // 21
    let mut numbers = Vec::with_capacity(n);
    for _ in 0..n {
        let val = (lcg.next() % range) as i32 + min_val;
        numbers.push(val);
    }

    let mut max_sum: i32 = i32::MIN;
    for i in 0..n {
        let mut current_sum: i32 = 0;
        for j in i..n {
            current_sum += numbers[j];
            if current_sum > max_sum {
                max_sum = current_sum;
            }
        }
    }
    max_sum
}

fn total_max_subarray_sum(n: usize, initial_seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut lcg = Lcg::new(initial_seed);
    let mut total: i64 = 0;
    for _ in 0..20 {
        let seed = lcg.next();
        let sub_sum = max_subarray_sum(n, seed, min_val, max_val);
        total += sub_sum as i64;
    }
    total
}

fn main() {
    // Parameters
    let n = 10_000;
    let initial_seed = 42u32;
    let min_val = -10i32;
    let max_val = 10i32;

    let start = Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let duration = start.elapsed();
    let secs = duration.as_secs_f64();

    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6} seconds", secs);
}

