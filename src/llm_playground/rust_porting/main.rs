use std::time::Instant;

// Constants for LCG
const A: u64 = 1664525;
const C: u64 = 1013904223;
const M: u64 = 1u64 << 32;

struct Lcg {
    state: u64,
}

impl Lcg {
    #[inline(always)]
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    #[inline(always)]
    fn next(&mut self) -> u64 {
        self.state = self.state.wrapping_mul(A).wrapping_add(C) % M;
        self.state
    }
}

// Kadane's algorithm for max subarray sum
#[inline(always)]
fn max_subarray_sum(arr: &[i32]) -> i32 {
    let mut max_ending_here = arr[0];
    let mut max_so_far = arr[0];
    for &x in &arr[1..] {
        max_ending_here = max_ending_here.saturating_add(x).max(x);
        max_so_far = max_so_far.max(max_ending_here);
    }
    max_so_far
}

// Generates the random numbers and finds max subarray sum
fn max_subarray_sum_for_seed(n: usize, seed: u64, min_val: i32, max_val: i32) -> i32 {
    let range = (max_val - min_val + 1) as u64;

    let mut lcg = Lcg::new(seed);

    // Preallocate vector with capacity n
    let mut random_numbers = Vec::with_capacity(n);
    for _ in 0..n {
        // We cast lcg.next() to i32 range (min_val..max_val)
        let val = (lcg.next() % range) as i32 + min_val;
        random_numbers.push(val);
    }
    max_subarray_sum(&random_numbers)
}

fn total_max_subarray_sum(n: usize, initial_seed: u64, min_val: i32, max_val: i32) -> i64 {
    let mut total_sum: i64 = 0;
    let mut lcg = Lcg::new(initial_seed);

    for _ in 0..20 {
        let seed = lcg.next();
        let max_sum = max_subarray_sum_for_seed(n, seed, min_val, max_val);
        total_sum += max_sum as i64;
    }
    total_sum
}

fn main() {
    let n = 10_000;
    let initial_seed = 42;
    let min_val = -10;
    let max_val = 10;

    let start = Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let elapsed = start.elapsed();

    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6} seconds", elapsed.as_secs_f64());
}