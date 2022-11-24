let string_grid = "08";

let list_of_line = [];
let grid = [];
let string_number = "";

for (let i = 0; i < string_grid.length; i++) {
  if ((i + 1) % 3 !== 0) {
    string_number = string_number + string_grid[i];
  }
  if (string_number.length === 2) {
    if (string_number[0] === "0") {
      string_number = string_number[1];
    }
    list_of_line.push(Number(string_number));
    string_number = "";
  }
  if (list_of_line.length === 20) {
    grid.push(list_of_line);
    list_of_line = [];
  }


function vertical_product(grid, n_number) {
  let biggest_product = 0;
  let product = 1;
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid.length - (n_number - 1); j++) {
      product = 1;
      for (let x = 0; x < n_number; x++) {
        product *= grid[i][j + x];
      }
      if (product > biggest_product) {
        biggest_product = product;
      }
    }
  }
  return biggest_product;
}

function horizontal_product(grid, n_number) {
  let biggest_product = 0;
  let product = 1;
  for (let i = 0; i < grid.length - (n_number - 1); i++) {
    for (let j = 0; j < grid.length; j++) {
      product = 1;
      for (let x = 0; x < n_number; x++) {
        product *= grid[i + x][j];
      }
      if (product > biggest_product) {
        biggest_product = product;
      }
    }
  }
  return biggest_product;
}

function product_of_a_grid(grid, n_number, direction) {
  let biggest_product = 0;
  let product = 1;

  for (let i = start_i; i < grid.length - horizontal_subtractor; i++) {
    for (let j = start_j; j < grid.length - vertical_subtractor; j++) {
      product = 1;
      let in_x = 0;
      let in_y = 0;
      for (let n = 0; n < n_number; n++) {
        product *= grid[i + in_x][j + in_y];
        in_x += x;
        in_y += y;
      }
      if (product > biggest_product) {
        biggest_product = product;
      }
    }
  }
  return biggest_product;
}

function largest_product_of_grid(grid, n_number) {
  let directions = ["v", "h", "d_l", "d_r"];
  let biggest_product = 0;
  for (let i = 0; i < directions.length; i++) {
    direction = directions[i];
    product = product_of_a_grid(grid, 4, direction);
    if (product > biggest_product) {
      biggest_product = product;
    }
  }
  return biggest_product;
}

console.log(largest_product_of_grid(grid, 4));
