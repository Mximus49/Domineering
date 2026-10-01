% GENEROS MUSICALES
genero(rock).
genero(rock_latino).
genero(rock_alternativo).
genero(grunge).
genero(hard_rock).
genero(pop_rock).
genero(rock_progresivo).
genero(metal).
genero(heavy_metal).
genero(nu_metal).
genero(electronica).
genero(house_frances).

% JERARQUIA DE GENEROS
% subgenero(subgenero, genero_padre)
subgenero(rock_latino, rock).
subgenero(rock_alternativo, rock).
subgenero(grunge, rock_alternativo).
subgenero(hard_rock, rock).
subgenero(pop_rock, rock).
subgenero(rock_progresivo, rock).
subgenero(metal, rock).
subgenero(heavy_metal, metal).
subgenero(nu_metal, metal).
subgenero(house_frances, electronica).

% BANDAS
% banda(nombre_banda, genero, pais, anio_formacion, estado)
% estado: activa | separada
banda(los_prisioneros, rock_latino, chile, 1983, separada).
banda(los_tres, rock_latino, chile, 1987, activa).
banda(soda_stereo, rock_latino, argentina, 1982, separada).
banda(nirvana, grunge, estados_unidos, 1987, separada).
banda(foo_fighters, rock_alternativo, estados_unidos, 1994, activa).
banda(linkin_park, nu_metal, estados_unidos, 1996, activa).
banda(metallica, heavy_metal, estados_unidos, 1981, activa).
banda(queen, hard_rock, reino_unido, 1970, activa).
banda(radiohead, rock_alternativo, reino_unido, 1985, activa).
banda(the_beatles, pop_rock, reino_unido, 1960, separada).
banda(pink_floyd, rock_progresivo,  reino_unido, 1965, separada).
banda(daft_punk, house_frances, francia, 1993, separada).

% MIEMBROS
% miembro(persona, banda, rol_principal, estado)
% estado: actual (formacion actual o la ultima, si la banda se separo) | ex

% --- LOS PRISIONEROS ---
miembro(jorge_gonzalez, los_prisioneros, voz, actual).
miembro(miguel_tapia, los_prisioneros, bateria, actual).
miembro(claudio_narea, los_prisioneros, guitarra, ex).
miembro(cecilia_aguayo, los_prisioneros, teclado,  ex).
miembro(alvaro_henriquez, los_prisioneros, guitarra, ex).

% --- LOS TRES ---
miembro(alvaro_henriquez, los_tres, voz, actual).
miembro(angel_parra, los_tres, guitarra, actual).
miembro(roberto_lindl, los_tres, bajo, actual).
miembro(francisco_molina, los_tres, bateria, actual).

% --- SODA STEREO ---
miembro(gustavo_cerati, soda_stereo, voz, actual).
miembro(zeta_bosio, soda_stereo, bajo, actual).
miembro(charly_alberti, soda_stereo, bateria, actual).

% --- NIRVANA ---
miembro(kurt_cobain, nirvana, voz, actual).
miembro(krist_novoselic, nirvana, bajo, actual).
miembro(dave_grohl, nirvana, bateria, actual).
miembro(chad_channing, nirvana, bateria, ex).

% --- FOO FIGHTERS ---
miembro(dave_grohl, foo_fighters, voz, actual).
miembro(pat_smear, foo_fighters, guitarra, actual).
miembro(nate_mendel, foo_fighters, bajo, actual).
miembro(chris_shiflett, foo_fighters, guitarra, actual).
miembro(rami_jaffee, foo_fighters, teclado, actual).
miembro(ilan_rubin, foo_fighters, bateria, actual).
miembro(taylor_hawkins, foo_fighters, bateria, ex).

% --- LINKIN PARK ---
miembro(emily_armstrong, linkin_park, voz, actual).
miembro(mike_shinoda, linkin_park, voz, actual).
miembro(joe_hahn, linkin_park, dj, actual).
miembro(colin_brittain, linkin_park, bateria, actual).
miembro(brad_delson, linkin_park, guitarra, actual).
miembro(dave_farrell, linkin_park, bajo, actual).
miembro(chester_bennington, linkin_park, voz, ex).
miembro(rob_bourdon, linkin_park, bateria, ex).
miembro(mark_wakefield, linkin_park, voz, ex).
miembro(kyle_christner, linkin_park, bajo, ex).

% --- METALLICA ---
miembro(james_hetfield, metallica, voz, actual).
miembro(lars_ulrich, metallica, bateria, actual).
miembro(kirk_hammett, metallica, guitarra, actual).
miembro(robert_trujillo, metallica, bajo, actual).
miembro(cliff_burton, metallica, bajo, ex).
miembro(jason_newsted, metallica, bajo, ex).
miembro(dave_mustaine, metallica, guitarra, ex).

% --- QUEEN ---
miembro(freddie_mercury, queen, voz, actual).
miembro(brian_may, queen, guitarra, actual).
miembro(roger_taylor, queen, bateria, actual).
miembro(john_deacon, queen, bajo, ex).

% --- RADIOHEAD ---
miembro(thom_yorke, radiohead, voz, actual).
miembro(jonny_greenwood, radiohead, guitarra, actual).
miembro(colin_greenwood, radiohead, bajo, actual).
miembro(ed_obrien, radiohead, guitarra, actual).
miembro(phil_selway, radiohead, bateria, actual).

% --- THE BEATLES ---
miembro(john_lennon, the_beatles, voz, actual).
miembro(paul_mccartney, the_beatles, bajo, actual).
miembro(george_harrison, the_beatles, guitarra, actual).
miembro(ringo_starr, the_beatles, bateria, actual).
miembro(pete_best, the_beatles, bateria, ex).
miembro(stuart_sutcliffe, the_beatles, bajo, ex).

% --- PINK FLOYD ---
miembro(david_gilmour, pink_floyd, guitarra, actual).
miembro(nick_mason, pink_floyd, bateria, actual).
miembro(richard_wright, pink_floyd, teclado, actual).
miembro(roger_waters, pink_floyd, bajo, ex).
miembro(syd_barrett, pink_floyd, guitarra, ex).

% --- DAFT PUNK ---
miembro(thomas_bangalter, daft_punk, sintetizador, actual).
miembro(guy_manuel_de_homem_christo, daft_punk, sintetizador, actual).

% ALBUMES
% album(titulo, banda, anio)

% --- LOS PRISIONEROS ---
album('La voz de los 80', los_prisioneros, 1984).
album('Pateando piedras', los_prisioneros, 1986).
album('La cultura de la basura', los_prisioneros, 1987).
album('Corazones', los_prisioneros, 1990).

% --- LOS TRES ---
album('Los Tres', los_tres, 1991).
album('La espada & la pared', los_tres, 1995).
album('MTV Unplugged', los_tres, 1996).

% --- SODA STEREO ---
album('Signos', soda_stereo, 1986).
album('Canción animal', soda_stereo, 1990).
album('Dynamo', soda_stereo, 1992).

% --- NIRVANA ---
album('Bleach', nirvana, 1989).
album('Nevermind', nirvana, 1991).
album('In Utero', nirvana, 1993).

% --- FOO FIGHTERS ---
album('Foo Fighters', foo_fighters, 1995).
album('The Colour and the Shape', foo_fighters, 1997).
album('Wasting Light', foo_fighters, 2011).

% --- LINKIN PARK ---
album('Hybrid Theory', linkin_park, 2000).
album('Meteora', linkin_park, 2003).
album('Minutes to Midnight', linkin_park, 2007).
album('From Zero', linkin_park, 2024).

% --- METALLICA ---
album('Master of Puppets', metallica, 1986).
album('Metallica', metallica, 1991).
album('72 Seasons', metallica, 2023).

% --- QUEEN ---
album('A Night at the Opera', queen, 1975).
album('News of the World', queen, 1977).
album('The Game', queen, 1980).

% --- RADIOHEAD ---
album('OK Computer', radiohead, 1997).
album('Kid A', radiohead, 2000).
album('In Rainbows', radiohead, 2007).

% --- THE BEATLES ---
album('Please Please Me', the_beatles, 1963).
album('Sgt. Peppers Lonely Hearts Club Band', the_beatles, 1967).
album('Abbey Road', the_beatles, 1969).

% --- PINK FLOYD ---
album('The Dark Side of the Moon', pink_floyd, 1973).
album('Wish You Were Here', pink_floyd, 1975).
album('The Wall', pink_floyd, 1979).

% --- DAFT PUNK ---
album('Homework', daft_punk, 1997).
album('Discovery', daft_punk, 2001).
album('Random Access Memories', daft_punk, 2013).

% CARRERA SOLISTA
% carrera_solista(persona)
carrera_solista(jorge_gonzalez).
carrera_solista(claudio_narea).
carrera_solista(alvaro_henriquez).
carrera_solista(angel_parra).
carrera_solista(gustavo_cerati).
carrera_solista(dave_grohl).
carrera_solista(pat_smear).
carrera_solista(nate_mendel).
carrera_solista(chris_shiflett).
carrera_solista(ilan_rubin).
carrera_solista(mike_shinoda).
carrera_solista(freddie_mercury).
carrera_solista(brian_may).
carrera_solista(roger_taylor).
carrera_solista(thom_yorke).
carrera_solista(jonny_greenwood).
carrera_solista(phil_selway).
carrera_solista(ed_obrien).
carrera_solista(john_lennon).
carrera_solista(paul_mccartney).
carrera_solista(george_harrison).
carrera_solista(ringo_starr).
carrera_solista(david_gilmour).
carrera_solista(roger_waters).
carrera_solista(syd_barrett).
carrera_solista(thomas_bangalter).

% FALLECIDOS
% fallecido(persona)
fallecido(kurt_cobain).
fallecido(freddie_mercury).
fallecido(chester_bennington).
fallecido(gustavo_cerati).
fallecido(taylor_hawkins).
fallecido(cliff_burton).
fallecido(john_lennon).
fallecido(george_harrison).
fallecido(stuart_sutcliffe).
fallecido(richard_wright).
fallecido(syd_barrett).

% INFLUENCIAS
% influyo(banda_a, banda_b): banda_a influyo directamente en banda_b
influyo(the_beatles, nirvana).
influyo(the_beatles, soda_stereo).
influyo(the_beatles, queen).
influyo(pink_floyd, radiohead).
influyo(queen, metallica).
influyo(nirvana, foo_fighters).

% Variable Fija
anio_actual(2026).

% REGLAS

% Formo parte de la banda en algun momento
integrante(P, B) :- miembro(P, B, _, _).
miembro_actual(P, B) :- miembro(P, B, _, actual).
exmiembro(P, B) :- miembro(P, B, _, ex).
exmiembro_vivo(P, B) :- exmiembro(P, B), \+ fallecido(P).

% Rol que cumple una persona (en cualquier banda)
toca(P, Rol) :- miembro(P, _, Rol, _).

% Jerarquia de generos (transitiva)
pertenece_a(G1, G2) :- subgenero(G1, G2).
pertenece_a(G1, G2) :- subgenero(G1, G3), pertenece_a(G3, G2).

% Estilo de una banda: su genero y todos los generos padre
estilo(B, G) :- banda(B, G, _, _, _).
estilo(B, G) :- banda(B, S, _, _, _), pertenece_a(S, G).

% Datos de la banda
pais_de(B, P) :- banda(B, _, P, _, _).
banda_activa(B) :- banda(B, _, _, _, activa).
banda_separada(B) :- banda(B, _, _, _, separada).
mismo_pais(A, B) :- pais_de(A, P), pais_de(B, P), A \= B.

% Compañeros de banda
companeros(A, B) :- integrante(A, X), integrante(B, X), A \= B.

% Persona que estuvo en 2 o mas bandas
varias_bandas(P) :-
    setof(B, integrante(P, B), L), length(L, N), N >= 2.

% Integrante de una banda que ademas tuvo carrera solista
solista_de_banda(P, B) :- integrante(P, B), carrera_solista(P).

% Influencia directa o indirecta
influencia(A, B) :- influyo(A, B).
influencia(A, C) :- influyo(A, B), influencia(B, C).

% Decada en que una banda saco discos
activa_en_decada(B, D) :- album(_, B, Y), D is (Y // 10) * 10.

% Album clasico: 30 o mas años
antiguedad(T, N) :- album(T, _, Y), anio_actual(H), N is H - Y.
clasico(T) :- antiguedad(T, N), N >= 30.

% Cantidad de álbumes de una banda
cantidad_albumes(B, N) :-
    banda(B, _, _, _, _),
    aggregate_all(count, album(_, B, _), N).

% Años desde la formación de la banda
trayectoria(B, N) :-
    banda(B, _, _, Y, _), anio_actual(H), N is H - Y.

% Reemplazo: un exmiembro y un miembro actual con el mismo rol en la misma banda
reemplazo(Ex, Nuevo, B) :-
    miembro(Ex, B, Rol, ex),
    miembro(Nuevo, B, Rol, actual).

% Integrantes fallecidos de una banda
fallecido_de(P, B) :- integrante(P, B), fallecido(P).

% Banda que sigue activa a pesar de haber perdido a un integrante
banda_superviviente(B) :-
    banda_activa(B), fallecido_de(_, B).

% Cantantes (cualquier persona cuyo rol sea voz)
cantante(P) :- miembro(P, _, voz, _).


% OPCIONES DE PREGUNTAS
% ---------------------------- HECHOS ----------------------------

% ¿Que generos hay en la KB?
% ?- genero(G).

% ¿Que subgeneros tiene el rock (directos)?
% ?- subgenero(S, rock).
%    rock_latino, rock_alternativo, hard_rock, pop_rock, rock_progresivo, metal

% Todos los datos de Linkin Park
% ?- banda(linkin_park, Genero, Pais, Anio, Estado).
%    Genero = nu_metal, Pais = estados_unidos, Anio = 1996, Estado = activa

% ¿Que bandas son de Chile?
% ?- banda(B, _, chile, _, _).
%    los_prisioneros, los_tres

% ¿Quienes son los miembros actuales de Queen?
% ?- miembro(P, queen, _, actual).
%    freddie_mercury, brian_may, roger_taylor

% ¿Que albumes tiene Los Prisioneros y de que año?
% ?- album(T, los_prisioneros, A).
%    'La voz de los 80' 1984, 'Pateando piedras' 1986,
%    'La cultura de la basura' 1987, 'Corazones' 1990

% ¿Mike Shinoda tiene carrera solista?
% ?- carrera_solista(mike_shinoda).
%    true

% ¿John Deacon fallecio?
% ?- fallecido(john_deacon).
%    false

% ¿En quienes influyeron directamente The Beatles?
% ?- influyo(the_beatles, X).
%    nirvana, soda_stereo, queen

% ---------------------------- REGLAS ----------------------------

% integrante: ¿quienes formaron parte de Nirvana alguna vez?
% ?- integrante(P, nirvana).
%    kurt_cobain, krist_novoselic, dave_grohl, chad_channing

% miembro_actual: formacion actual de Linkin Park
% ?- miembro_actual(P, linkin_park).
%    emily_armstrong, mike_shinoda, joe_hahn, colin_brittain,
%    brad_delson, dave_farrell

% exmiembro: exmiembros de Metallica
% ?- exmiembro(P, metallica).
%    cliff_burton, jason_newsted, dave_mustaine

% exmiembro_vivo: exmiembros de Linkin Park que siguen vivos
% ?- exmiembro_vivo(P, linkin_park).
%    rob_bourdon, mark_wakefield, kyle_christner

% toca: ¿que roles cumple Dave Grohl?
% ?- toca(dave_grohl, R).
%    bateria (Nirvana), voz (Foo Fighters)

% pertenece_a: ¿a que generos pertenece el grunge?
% ?- pertenece_a(grunge, G).
%    rock_alternativo, rock

% pertenece_a: ¿el nu_metal es rock? (2 niveles de jerarquia)
% ?- pertenece_a(nu_metal, rock).
%    true

% estilo: todos los estilos de Nirvana
% ?- estilo(nirvana, G).
%    grunge, rock_alternativo, rock

% estilo: ¿que bandas son de metal (incluyendo subgeneros)?
% ?- estilo(B, metal).
%    linkin_park, metallica

% pais_de: ¿de donde es Daft Punk?
% ?- pais_de(daft_punk, P).
%    francia

% banda_activa / banda_separada
% ?- banda_activa(B).
%    los_tres, foo_fighters, linkin_park, metallica, queen, radiohead
% ?- banda_separada(B).
%    los_prisioneros, soda_stereo, nirvana, the_beatles, pink_floyd, daft_punk

% mismo_pais: ¿que bandas son del mismo pais que Los Prisioneros?
% ?- mismo_pais(los_prisioneros, B).
%    los_tres

% companeros: compañeros de banda de Kurt Cobain
% ?- companeros(kurt_cobain, X).
%    krist_novoselic, dave_grohl, chad_channing

% varias_bandas: ¿quien estuvo en mas de una banda?
% ?- varias_bandas(P).
%    alvaro_henriquez, dave_grohl

% solista_de_banda: integrantes de Radiohead con carrera solista
% ?- solista_de_banda(P, radiohead).
%    thom_yorke, jonny_greenwood, phil_selway, ed_obrien

% influencia: influencia directa e indirecta de The Beatles
% ?- influencia(the_beatles, X).
%    nirvana, soda_stereo, queen, foo_fighters, metallica

% influencia: ¿quienes influyeron en Foo Fighters?
% ?- influencia(X, foo_fighters).
%    nirvana, the_beatles

% activa_en_decada: bandas que sacaron discos en los 90 (sin repetidos)
% ?- setof(B, activa_en_decada(B, 1990), L).
%    L = [daft_punk, foo_fighters, los_prisioneros, los_tres,
%         metallica, nirvana, radiohead, soda_stereo]

% antiguedad: ¿cuantos años tiene Nevermind?
% ?- antiguedad('Nevermind', N).
%    N = 35

% antiguedad: albumes de Linkin Park con su antiguedad
% ?- album(T, linkin_park, _), antiguedad(T, N).
%    'Hybrid Theory' 26, 'Meteora' 23, 'Minutes to Midnight' 19, 'From Zero' 2

% antiguedad: albumes con 50 años o mas
% ?- antiguedad(T, N), N >= 50.
%    'A Night at the Opera' 51, 'Please Please Me' 63,
%    'Sgt. Peppers Lonely Hearts Club Band' 59, 'Abbey Road' 57,
%    'The Dark Side of the Moon' 53, 'Wish You Were Here' 51

% clasico
% ?- clasico('Nevermind').
%    true
% ?- clasico('Hybrid Theory').
%    false

% cantidad_albumes: ¿cuantos albumes tiene Linkin Park?
% ?- cantidad_albumes(linkin_park, N).
%    N = 4

% cantidad_albumes: bandas con 4 o mas albumes en la KB
% ?- cantidad_albumes(B, N), N >= 4.
%    los_prisioneros 4, linkin_park 4

% trayectoria: años desde la formacion de Queen
% ?- trayectoria(queen, N).
%    N = 56

% reemplazo: reemplazos en Foo Fighters
% ?- reemplazo(Ex, Nuevo, foo_fighters).
%    Ex = taylor_hawkins, Nuevo = ilan_rubin

% reemplazo: ¿a quien reemplazo Robert Trujillo?
% ?- reemplazo(Ex, robert_trujillo, metallica).
%    cliff_burton, jason_newsted

% reemplazo: banda sin reemplazos (Deacon es bajo y no hay bajista actual)
% ?- reemplazo(Ex, Nuevo, queen).
%    false

% fallecido_de: integrantes fallecidos de The Beatles
% ?- fallecido_de(P, the_beatles).
%    john_lennon, george_harrison, stuart_sutcliffe

% banda_superviviente: bandas activas que perdieron a un integrante
% ?- banda_superviviente(B).
%    foo_fighters, linkin_park, metallica, queen

% cantante
% ?- cantante(dave_grohl).
%    true

% ------------------------ CONSULTAS COMBINADAS ------------------------

% Cantantes fallecidos
% ?- cantante(P), fallecido(P).
%    gustavo_cerati, kurt_cobain, chester_bennington, freddie_mercury, john_lennon

% Personas con carrera solista que fallecieron
% ?- carrera_solista(P), fallecido(P).
%    gustavo_cerati, freddie_mercury, john_lennon, george_harrison, syd_barrett

% Bandas chilenas que siguen activas
% ?- banda(B, _, chile, _, activa).
%    los_tres

% Todos los albumes de una banda en una lista
% ?- findall(T, album(T, queen, _), L).
%    L = ['A Night at the Opera', 'News of the World', 'The Game']
