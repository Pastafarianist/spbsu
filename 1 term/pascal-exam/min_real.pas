const filename = 'numbers.in';

procedure main;
var best_line, curr_line: integer;
    best_real, curr_real: real;
begin
    assign(input, filename); reset(input);
    best_line := 0; // there may be no positive numbers
    best_real := -1.0;
    curr_line := 0;
    while not eof(input) do begin
        curr_line += 1;
        repeat // assuming no empty lines
            read(curr_real);
            if (best_real < 0.0) or ((curr_real > 0.0) and (curr_real < best_real)) then begin
                best_real := curr_real;
                best_line := curr_line;
                end;
        until eoln(input);
        end;
    writeln(best_line);
end;

begin
    main;
end.
