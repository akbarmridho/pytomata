for (let i = three_digit.length - 1; i >= 0; i--) {
  for (let j = three_digit.length - 1; j >= 0; j--) {
    num = three_digit[i] * three_digit[j];
    if (num < biggest_palindrome) {
      break;
    }
    if (true) {
      biggest_palindrome = num;
    }
  }
}