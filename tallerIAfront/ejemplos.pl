% EJEMPLOS DE TRADUCCION PREGUNTA -> CONSULTA
% chatbot.py le pasa estos ejemplos al LLM para que aprenda a traducir preguntas a Prolog.
% Formato: una linea "% pregunta" seguida de una linea "% ?- consulta."
% Si una pregunta se traduce mal, agregar aqui la pregunta con su consulta correcta.
% (Este archivo es solo de comentarios: Prolog no lo carga.)

% ---------------------------- HECHOS ----------------------------

% ¿Que generos hay en la KB?
% ?- genero(G).

% ¿Que subgeneros tiene el rock (directos)?
% ?- subgenero(S, rock).

% Todos los datos de Linkin Park
% ?- banda(linkin_park, Genero, Pais, Anio, Estado).

% ¿Que bandas son de Chile?
% ?- banda(B, _, chile, _, _).

% ¿Quienes son los miembros actuales de Queen?
% ?- miembro(P, queen, _, actual).

% ¿Que albumes tiene Los Prisioneros y de que año?
% ?- album(T, los_prisioneros, A).

% ¿Mike Shinoda tiene carrera solista?
% ?- carrera_solista(mike_shinoda).

% ¿John Deacon fallecio?
% ?- fallecido(john_deacon).

% ¿En quienes influyeron directamente The Beatles?
% ?- influyo(the_beatles, Influenciado).

% ---------------------------- REGLAS ----------------------------

% integrante: ¿quienes formaron parte de Nirvana alguna vez?
% ?- integrante(P, nirvana).

% miembro_actual: formacion actual de Linkin Park
% ?- miembro_actual(P, linkin_park).

% exmiembro: exmiembros de Metallica
% ?- exmiembro(P, metallica).

% exmiembro_vivo: exmiembros de Linkin Park que siguen vivos
% ?- exmiembro_vivo(P, linkin_park).

% toca: ¿que roles cumple Dave Grohl?
% ?- toca(dave_grohl, R).

% pertenece_a: ¿a que generos pertenece el grunge?
% ?- pertenece_a(grunge, G).

% pertenece_a: ¿el nu_metal es rock? (2 niveles de jerarquia)
% ?- pertenece_a(nu_metal, rock).

% estilo: todos los estilos de Nirvana
% ?- estilo(nirvana, G).

% estilo: ¿que bandas son de metal (incluyendo subgeneros)?
% ?- estilo(B, metal).

% pais_de: ¿de donde es Daft Punk?
% ?- pais_de(daft_punk, P).

% banda_activa / banda_separada
% ?- banda_activa(B).
% ?- banda_separada(B).

% mismo_pais: ¿que bandas son del mismo pais que Los Prisioneros?
% ?- mismo_pais(los_prisioneros, B).

% companeros: compañeros de banda de Kurt Cobain
% ?- companeros(kurt_cobain, X).

% varias_bandas: ¿quien estuvo en mas de una banda?
% ?- varias_bandas(P).

% solista_de_banda: integrantes de Radiohead con carrera solista
% ?- solista_de_banda(P, radiohead).

% influencia: influencia directa e indirecta de The Beatles
% ?- influencia(the_beatles, Influenciado).

% influencia: ¿quienes influyeron en Foo Fighters?
% ?- influencia(Influyente, foo_fighters).

% activa_en_decada: bandas que sacaron discos en los 90 (sin repetidos)
% ?- setof(B, activa_en_decada(B, 1990), L).

% antiguedad: ¿cuantos años tiene Nevermind?
% ?- antiguedad('Nevermind', N).

% antiguedad: albumes de Linkin Park con su antiguedad
% ?- album(T, linkin_park, _), antiguedad(T, N).

% antiguedad: albumes con 50 años o mas
% ?- antiguedad(T, N), N >= 50.

% clasico
% ?- clasico('Nevermind').

% cantidad_albumes: ¿cuantos albumes tiene Linkin Park?
% ?- cantidad_albumes(linkin_park, N).

% cantidad_albumes: bandas con 4 o mas albumes en la KB
% ?- cantidad_albumes(B, N), N >= 4.

% trayectoria: años desde la formacion de Queen
% ?- trayectoria(queen, N).

% reemplazo: reemplazos en Foo Fighters
% ?- reemplazo(Ex, Nuevo, foo_fighters).

% reemplazo: ¿a quien reemplazo Robert Trujillo?
% ?- reemplazo(Ex, robert_trujillo, metallica).

% fallecido_de: integrantes fallecidos de The Beatles
% ?- fallecido_de(P, the_beatles).

% banda_superviviente: bandas activas que perdieron a un integrante
% ?- banda_superviviente(B).

% cantante
% ?- cantante(dave_grohl).

% ------------------------ CONSULTAS COMBINADAS ------------------------

% Cantantes fallecidos
% ?- cantante(P), fallecido(P).

% Personas con carrera solista que fallecieron
% ?- carrera_solista(P), fallecido(P).

% Bandas chilenas que siguen activas
% ?- banda(B, _, chile, _, activa).

% Todos los albumes de una banda en una lista
% ?- findall(T, album(T, queen, _), L).

% Albumes clasicos de una banda
% ?- album(T, metallica, _), clasico(T).

% Ex miembros que estuvieron en mas de una banda, y en cuales
% ?- exmiembro(P, _), varias_bandas(P), findall(B, integrante(P, B), Bandas).

% ¿En que bandas estuvo Alvaro Henriquez?
% ?- integrante(alvaro_henriquez, B).

% ¿Quienes de Pink Floyd tuvieron carrera solista?
% ?- solista_de_banda(P, pink_floyd).

% ¿Quienes de Queen fallecieron?
% ?- fallecido_de(P, queen).

% ¿En quienes influyo Queen? (Queen es quien influye: va primero)
% ?- influyo(queen, Influenciado).

% ¿Quien influyo en Radiohead? (Radiohead es el influenciado: va segundo)
% ?- influyo(Influyente, radiohead).

% ¿Quien es el guitarrista de Radiohead? (rol de una banda: miembro/4)
% ?- miembro(P, radiohead, guitarra, actual).

% ¿Quien tocaba el bajo en Nirvana? (en cualquier epoca: estado _)
% ?- miembro(P, nirvana, bajo, _).

% ¿Que bandas son de grunge? (genero o subgenero: estilo/2)
% ?- estilo(B, grunge).

% ¿A quien reemplazo Ilan Rubin? (sin saber la banda)
% ?- reemplazo(Ex, ilan_rubin, B).

% ¿Que cantantes siguen vivos?
% ?- cantante(P), \+ fallecido(P).

% Canciones de Queen (la base no tiene canciones, solo albumes: consulta vacia)
% ?- .
