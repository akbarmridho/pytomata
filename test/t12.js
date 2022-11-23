let triangle_number = 1;
let increment = 1;

function nth_triangle(n) {
  let result = 0;
  for (let i = 0; i <= n; i++) {
    result += i;
  }
  return result;
}

const n_of_divisor = (num) => {
  let small_factors = [1, 2, 2, 3, 2, 4];
  if (num <= 6) {
    return small_factors[num - 1];
  }
  let number_of_divisor = 0;
  let possible_divisor = [];
  for (let i = 0; i <= Math.ceil(num ** 0.5); i++) {
    if (num % i === 0) {
      if (i !== num / i) {
        number_of_divisor += 2;
      } else {
        number_of_divisor += 1;
      }
    }
  }
  return number_of_divisor;
};

while (n_of_divisor(triangle_number) <= 500) {
  increment++;
  triangle_number += increment;
}

//console.log(n_of_divisor())
console.log(triangle_number);
//console.log(nth_triangle(4));
