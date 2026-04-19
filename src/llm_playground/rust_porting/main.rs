use std::io::{self, Write};
use std::time::Instant;

const A: u32 = 1_664_525;
const C: u32 = 1_013_904_223;
const RUNS: usize = 20;

#[inline(always)]
fn next_lcg(state: &mut u32) -> u32 {
    *state = state.wrapping_mul(A).wrapping_add(C);
    *state
}

// Same result as the quadratic Python version, but O(n) via Kadane's algorithm.
#[inline(always)]
fn max_subarray_sum(n: usize, seed: u32, min_val: i64, range: u64) -> i64 {
    let mut state = seed;

    let first = (next_lcg(&mut state) as u64 % range) as i64 + min_val;
    let mut best_ending = first;
    let mut best = first;

    let mut i = 1usize;
    while i < n {
        let x = (next_lcg(&mut state) as u64 % range) as i64 + min_val;
        let sum = best_ending + x;
        best_ending = if sum > x { sum } else { x };
        if best_ending > best {
            best = best_ending;
        }
        i += 1;
    }

    best
}

#[inline(always)]
fn total_max_subarray_sum(n: usize, initial_seed: u32, min_val: i64, max_val: i64) -> i64 {
    let range = (max_val - min_val + 1) as u64;
    let mut total = 0i64;
    let mut outer_state = initial_seed;

    let mut i = 0usize;
    while i < RUNS {
        let seed = next_lcg(&mut outer_state);
        total += max_subarray_sum(n, seed, min_val, range);
        i += 1;
    }

    total
}

fn main() {
    let n = 10_000usize;
    let initial_seed = 42u32;
    let min_val = -10i64;
    let max_val = 10i64;

    let start_time = Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let elapsed = start_time.elapsed().as_secs_f64();

    let mut out = io::BufWriter::new(io::stdout().lock());
    writeln!(out, "Total Maximum Subarray Sum (20 runs): {}", result).unwrap();
    writeln!(out, "Execution Time: {:.6} seconds", elapsed).unwrap();
}