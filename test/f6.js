let upper_bound = 100

let sum_of_square = 0;
let square_of_sum = (upper_bound*(upper_bound+1)/2)**2;

for (let i = 1; i <= upper_bound;i++){
	sum_of_square += i**2
}

console.log(square_of_sum-sum_of_square)
