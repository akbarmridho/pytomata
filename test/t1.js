let N = 1000;

const sum_of_3 =
  (Math.floor(N / 3) * (2 * 3 + (Math.floor(N / 3) - 1) * 3)) / 2;

console.log(sum_of_3);
