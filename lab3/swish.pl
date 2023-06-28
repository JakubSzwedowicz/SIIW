% Początek drzewa struktury serwera. Server - podzespół
component(server, processor).
component(server, memory).
component(server, hard_drive).
component(server, optical_drive).
component(server, tape_backup_unit).
component(server, internal_usb_key).
component(server, sd_card).
component(server, storage_controller).
component(server, expansion_card).

% Elementy podzespołów
component(processor, core).
component(memory, dimm_socket).
component(hard_drive, platter).
component(hard_drive, read_write_head).
component(optical_drive, laser).
component(optical_drive, motor).
component(tape_backup_unit, tape_cartridge).
component(internal_usb_key, usb_connector).
component(sd_card, sd_card_slot).
component(storage_controller, controller_card).
component(expansion_card, expansion_card_slot).

% Potencjalne problemy i symptomy jakie mgoą wystąpić w serwerze
problem(memory_failure, memory_error_detected).
problem(memory_failure, system_does_not_boot).
problem(memory_failure, system_unstable).
problem(memory_failure, error_message_in_screen).

problem(internal_usb_key_failure, usb_key_not_detected).
problem(internal_usb_key_failure, error_message_on_screen).

problem(sd_card_failure, sd_card_not_detected).
problem(sd_card_failure, error_message_on_screen).

problem(optical_drive_failure, optical_drive_not_detected).
problem(optical_drive_failure, error_message_on_screen).

problem(tape_backup_unit_failure, tape_backup_unit_not_deteected).
problem(tape_backup_unit_failure, error_message_on_screen).

problem(hard_drive_failure, hard_drive_not_detected).

% Potencjalne czynności jakie trzeba wykonać w celu rozwiązania problemu
solution(memory_failure, run_diagnostic_test).
solution(memory_failure, check_memory_channels).
solution(memory_failure, reseat_memory_modules).
solution(memory_failure, replace_memory_module).
solution(internal_usb_key_failure, enter_system_setup).
solution(internal_usb_key_failure, reseat_usb_key).
solution(internal_usb_key_failure, check_usb_key_function).
solution(sd_card_failure, ensure_sd_card_port_enabled).
solution(sd_card_failure, replace_failed_sd_card).
solution(sd_card_failure, check_sd_card_function).

% Cechy poszczególnych peryferiów.
% Wskazują na parametry serwera na które mają wpływ poszczególne perfyeria.
% Np. na dostępne interfejsy urządzenia wpływają storage_controller oraz expansion_card
property(processor, clock_speed).
property(memory, capacity).
property(hard_drive, storage_capacity).
property(optional_drive, read_speed).
property(tape_backup_unit, storage_capacity).
property(internal_usb_key, storage_capacity).
property(sd_card, storage_capacity).
property(storage_controller, interace_type).
property(expansion_card, interface_type).

% Relacje opisujące który problem dotyczy którego peryferium lub jego elementu
affects(memory_failure, memory).
affects(internal_usb_key_failure, usb_connector).
affects(sd_card_failure, sd_card).
affects(optional_drive_failure, optical_drive).
affects(tape_backup_failure, tape_cartridge).

% Zapytania
affects_components(Problem, Component) :- 
    affects(Problem, Component).
affects_components(Problem, Component) :- 
    affects(Problem, Perypherial),
    component(Perypherial, Component).
% ?- affects_components(hard_drive_failure, component).

possible_problems(Symptoms) :- 
    setof(Problem, Symptom^(member(Symptom, Symptoms), problem(Problem, Symptom)), Problems),
    maplist(format("~w~n"), Problems).
% ?- possible_problems([error_message_on_screen, memory_error_detected]).

symptoms_for_component(Component) :-
    setof(Symptom, Problem^(affects(Problem, Component), problem(Problem, Symptom)), Symptoms),
    maplist(format("~w~n"), Symptoms).
% ?- symptoms_for_component(hard_drive).
