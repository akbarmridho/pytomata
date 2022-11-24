let digit = 3;

function is_palindrome(num) {
  const string_num = num.toString();
  const stopping_point = Math.floor(string_num.length / 2);
  //console.log(stopping_point)
  for (let i = 0; i <= stopping_point; i++) {
    if (string_num[i] !== string_num[string_num.length - 1 - i]) {
      return false;
    }
  }
  return true;
}

let palindrome_and_constructor = [];
let biggest_palindrome = 0;
let three_digit = [];

for (let i = 10 ** 2; i < 10 ** 3; i++) {
  three_digit.push(i);
}

for (let i = three_digit.length - 1; i >= 0; i--) {
  for (let j = three_digit.length - 1; j >= 0; j--) {
    num = three_digit[i] * three_digit[j];
    if (num < biggest_palindrome) {
      break;
    }
    if (is_palindrome(num)) {
      biggest_palindrome = num;
    }
  }
}

console.log(biggest_palindrome);
