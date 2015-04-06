const MAX_N = 100;
type matrix = array [1..MAX_N, 1..MAX_N] of integer;

function symmetric(var a: matrix; n: integer): integer;
var i, j: integer;
begin
    symmetric := 0;
    for i := 1 to n - 1 do
        for j := i + 1 to n do
            if a[i, j] = a[j, i] then symmetric += 1;
end;

procedure main;
var n: integer;
    a: matrix;
    i, j: integer;
begin
    read(n);
    for i := 1 to n do
        for j := 1 to n do
            read(a[i, j]);
    writeln(symmetric(a, n));
end;

begin
    main;
end.
