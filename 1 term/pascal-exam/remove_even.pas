type
    PNode = ^Node;
    Queue = record
        first: PNode;
        last: PNode;
    end;
    Node = record
        val: integer;
        next: PNode;
    end;

procedure push(var q: Queue; v: integer);
var temp: PNode;
begin
    new(temp);
    temp^.val := v;
    temp^.next := nil;
    if q.first = nil then begin
        q.first := temp;
        q.last := temp;
    end else begin
        q.last^.next := temp;
        q.last := temp;
    end;
end;

procedure print_queue(q: Queue);
var qnode: PNode;
begin
    qnode := q.first;
    while qnode <> nil do begin
        write(qnode^.val, ' ');
        qnode := qnode^.next;
    end;
    writeln;
end;

procedure replace_with_next(var qnode: PNode);
var next_node: PNode;
begin
    next_node := qnode^.next;
    dispose(qnode);
    qnode := next_node;
end;

procedure remove_even(var q: Queue);
var qnode: PNode;
begin
    while (q.first <> nil) and (q.first^.val mod 2 = 0) do
        replace_with_next(q.first); // removing junk from beginning
    if q.first = nil then // nothing left
        q.last := nil
    else begin
        qnode := q.first; // selecting anchor
        while qnode^.next <> nil do // while something is in front of it
            if qnode^.next^.val mod 2 = 0 then // if the next node is bad
                replace_with_next(qnode^.next) // dump it
            else
                qnode := qnode^.next; // move anchor to the next node
        q.last := qnode;
    end;
end;

procedure main;
const n = 10;
var i: integer;
    q: Queue;
begin
    randomize;
    q.first := nil;
    q.last := nil;
    for i := 1 to n do
        push(q, random(9));
    print_queue(q);
    remove_even(q);
    print_queue(q);
end;

begin
    main;
end.
