var number_and_length = {};
let result = 0;
let longest_number_chain = [0, 0];

function chainlength(num) {
  let current_num = num;
  let length_of_chain = 1;
  while (current_num > 1) {
    if (number_and_length.hasOwnProperty(current_num)) {
      length_of_chain -= 1;
      length_of_chain += number_and_length[current_num];
      break;
    } else {
      if (current_num % 2 === 0) {
        current_num /= 2;
      } else {
        current_num = 3 * current_num + 1;
      }
      length_of_chain += 1;
    }
  }
  return length_of_chain;
}

for (let i = 1; i < 10 ** 6; i++) {
  length_of_chain = chainlength(i);
  if (length_of_chain > longest_number_chain[1]) {
    longest_number_chain = [i, length_of_chain];
  }
}

console.log(longest_number_chain);
