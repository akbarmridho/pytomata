const list_of_fibonacci = [1, 2];
let sum_of_even = list_of_fibonacci[list_of_fibonacci.length-1];
let next_fibonacci = 0;



while (list_of_fibonacci[list_of_fibonacci.length-1] < 4000000) {
	next_fibonacci = list_of_fibonacci[list_of_fibonacci.length-1]+list_of_fibonacci[list_of_fibonacci.length-2];
	list_of_fibonacci.push(next_fibonacci);
	if (next_fibonacci%2 === 0){
		sum_of_even += next_fibonacci;
	}
	
}

console.log (list_of_fibonacci)
console.log(sum_of_even);
