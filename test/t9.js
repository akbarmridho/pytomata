let target_perimeter = 1000
let found_perimeter = false;
let m = 2;
let perimeter = 0;

while (found_perimeter === false){
	for (let n = 2; n < m; n++){
		perimeter = 2*m*(m+n);
		if (perimeter === target_perimeter){
			found_perimeter = true;
			a = (m**2)+(n**2);
			b = 2*m*n;
			c = (m**2)-(n**2);
			console.log(a*b*c);
			break
		}
	}
	m++;
}

if (found_perimeter === false){
	console.log("Perimeter not found")
}
