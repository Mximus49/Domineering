% Puente entre Python y la base de conocimiento.
% Uso: swipl puente.pl "miembro(P, queen, _, actual)"
% Imprime una linea por solucion (Var = valor), "true" si se cumple sin variables
% o "false" si no hay soluciones.

:- use_module(library(sandbox)).
:- use_module(library(time)).
:- ensure_loaded(music_kb).

:- initialization(main, main).

main :-
    current_prolog_flag(argv, [Texto|_]),
    term_string(Consulta, Texto, [variable_names(Vars)]),
    safe_goal(Consulta),  % la consulta la escribe el LLM: no se permite nada peligroso (archivos, shell...)
    call_with_time_limit(3, findall(Vars, limit(50, Consulta), Sols)),
    list_to_set(Sols, Unicas),
    mostrar(Unicas).

mostrar([]) :- writeln(false).
mostrar([[]]) :- writeln(true).
mostrar(Sols) :-
    forall(member(S, Sols),
           ( forall((member(N = V, S), nonvar(V)), format("~w = ~q  ", [N, V])), nl )).
