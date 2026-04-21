
use std::time::Instant;

#[inline(always)]
fn lcg_next(value: u32) -> u32 {
    ((1664525_u64 * value as u64 + 1013904223) % (1u64 << 32)) as u32
}

#[inline(always)]
fn max_subarray_sum(n: usize, seed: u32, min_val: i32, max_val: i32) -> i64 {
    let range = (max_val - min_val + 1) as u32;
    
    // Pre-allocate and fill random numbers
    let mut nums = Vec::with_capacity(n);
    let mut val = seed;
    for _ in 0..n {
        val = lcg_next(val);
        nums.push((val % range) as i32 as i64 + min_val as i64);
    }
    
    // O(n^2) max subarray sum matching original algorithm
    let mut max_sum = i64::MIN;
    for i in 0..n {
        let mut cur_sum: i64 = 0;
        let nums_slice = &nums[i..];
        for &x in nums_slice.iter() {
            cur_sum += x;
            if cur_sum > max_sum {
                max_sum = cur_sum;
            }
        }
    }
    
    max_sum
}

#[inline(always)]
fn total_max_subarray_sum(n: usize, initial_seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut total = 0i64;
    let mut state = initial_seed;
    
    for _ in 0..20 {
        state = lcg_next(state);
        total += max_subarray_sum(n, state, min_val, max_val);
    }
    
    total
}

fn main() {
    let n = 10000;
    let initial_seed = 42u32;
    let min_val = -10i32;
    let max_val = 10i32;
    
    let start = Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let elapsed = start.elapsed();
    
    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6} seconds", elapsed.as_secs_f64());
}
