var point_and_path = {};

function point_path(x, y) {
  written_result = point_and_path[(x, y)];
  if (x === 1 || y === 1) {
    point_and_path[(x, y)] = 1;
  }
  if (written_result === null) {
    result = point_path(x - 1, y) + point_path(x, y - 1);
    point_and_path[(x, y)] = result;
    return result;
  } else {
    return written_result;
  }
}

//console.log(point_path(21, 21))
