:- use_module(library(scasp)).
:- use_module(library(lists)).
:- style_check(-singleton).
:- consult('data.pl').
:- include('data.pl').

% Accepted
action(helped_someone, 10).
action(donated_to_charity, 15).
action(lied, -5).
action(cheated, -10).
action(volunteered, 20).
action(stole, -20).
action(saved_a_life, 50).
action(harmed_someone, -30).
action(ate_pineapple_pizza, -200).
action(adopted_a_pet, 15).
action(went_to_work, 5).
action(saved_the_world, 200000).

% Rejected
action(rejected_helped_someone, -5).
action(rejected_donated_to_charity, -10).
action(rejected_lied, 5).
action(rejected_cheated, 10).
action(rejected_volunteered, -10).
action(rejected_stole, 10).
action(rejected_saved_a_life, -25).
action(rejected_harmed_someone, 15).
action(rejected_ate_pineapple_pizza, 200).
action(rejected_adopted_a_pet, -10).
action(rejected_went_to_work, -5).
action(rejected_saved_the_world, -200000).

% assume law abiding by default unless proven otherwise
law_abiding :- \+ violated_law.
violated_law :-
    actions(Actions),
    (member([stole, _], Actions);
    member([harmed_someone, _], Actions)).

check_law_abiding :-
    violated_law.
check_law_abiding.

find_morality(Total) :-
    collect(action(Actions),AllActs),
    calc_scores(AllActs,Total),
    write(Total),
    check_law_abiding,
    (law_abiding -> write(', you are law abiding'),nl; write(', you are not law abiding'),nl).

collect(Act,AllActs) :-
    collect_all(Act,AllActs,[]).

collect_all(Act,[Head|Rest],Acc) :-
    actions(Head),
    \+ member(Head,Acc),
    collect_all(Act,Rest,[Head|Acc]).
collect_all(_,[],_) :-
    !.

calc_scores([],0).
calc_scores([Head|Rest],Total) :-
    calc_actions(Head,0,NewTotal),
    calc_scores(Rest,AccTotal),
    Total is NewTotal + AccTotal.

% Calculate the total morality of a list of weighted actions
calc_actions([],Acc,Acc).  % Base case: empty list has total of 0
calc_actions([[Action, Number] | Rest], Acc, Total) :-
    weighted_morality(Action, Number, ActionTotal),  % Compute total for current action
    RestTotal is Acc + ActionTotal,
    calc_actions(Rest, RestTotal, Total).  % Recursively calculate for the rest

weighted_morality(Action, Number, Total) :-
    action(Action, Value),
    Total is Value * Number.

% % Example actions
% action(helped_someone, 10).
% action(stole, -20).
% action(rejected_stole, 5).
% action(rejected_helped_someone,-5).