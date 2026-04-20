// Be careful to support large numbers

// LCG function using u64 for larger number support and modulo arithmetic.
// The parameters a, c are typical for a multiplicative congruential generator.
// m is 2^32, which can be handled by u32 with implicit modulo, but using u64 for
// intermediate calculations prevents overflow before the modulo operation.
fn lcg(seed: u32, a: u64, c: u64, m: u64) -> impl Iterator<Item = u32> {
    let mut value = seed as u64;
    std::iter::from_fn(move || {
        value = (a * value + c) % m;
        Some(value as u32)
    })
}

// Kadane's algorithm for maximum subarray sum.
// It's O(n) and more efficient than the O(n^2) approach in the Python version.
// The problem statement implies the Python code should be ported directly,
// but for performance, Kadane's is the standard and fastest for this problem.
// To match the Python output exactly, we'd need to keep the O(n^2) loop.
// However, the prompt emphasizes "fastest possible implementation".
// Let's stick to the O(n^2) to ensure identical output, but acknowledge Kadane's.

fn max_subarray_sum(n: usize, seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut lcg_gen = lcg(seed, 1664525, 1013904223, 1 << 32);
    let range = (max_val - min_val + 1) as u32;

    // Generate random numbers using `take` and `map` for a more idiomatic Rust.
    // We use i64 for random_numbers to avoid overflow when summing.
    let random_numbers: Vec<i64> = lcg_gen
        .take(n)
        .map(|num| (num % range) as i64 + min_val as i64)
        .collect();

    let mut max_sum = i64::MIN; // Use i64::MIN for the smallest possible i64 value.

    // O(n^2) loop to exactly match the Python logic.
    for i in 0..n {
        let mut current_sum = 0i64;
        for j in i..n {
            current_sum += random_numbers[j];
            if current_sum > max_sum {
                max_sum = current_sum;
            }
        }
    }
    max_sum
}

// Calculate the total sum of max subarray sums over 20 runs.
fn total_max_subarray_sum(n: usize, initial_seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut total_sum = 0i64;
    let mut lcg_gen = lcg(initial_seed, 1664525, 1013904223, 1 << 32);

    for _ in 0..20 {
        let seed = lcg_gen.next().unwrap(); // unwrap is safe here because the generator is infinite.
        total_sum += max_subarray_sum(n, seed, min_val, max_val);
    }
    total_sum
}

fn main() {
    let n = 10000usize;         // Number of random numbers
    let initial_seed = 42u32; // Initial seed for the LCG
    let min_val = -10i32;     // Minimum value of random numbers
    let max_val = 10i32;      // Maximum value of random numbers

    // Use std::time::Instant for more precise timing.
    let start_time = std::time::Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let end_time = std::time::Instant::now();
    let duration = end_time.duration_since(start_time);

    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6} seconds", duration.as_secs_f64());
}