#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#Q:/65_PGM/65_PYT/game/game_v1f/actions.py
"""
Modul action má na starosti zpracování příkazů.
"""
print(f'===== Modul {__name__} ===== START')
############################################################################

from abc import ABCMeta, abstractmethod
from .   import world


############################################################################

def execute_command(command: str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
    """
    command = command.strip()   # Smaže úvodní a závěrečné bílé znaky
    if command == '':
        return _execute_empty_command()
    elif is_active:
        return _execute_standard_command(command)
    else:
        return ('Prvním příkazem není startovací příkaz.\n' +
                'Hru, která neběží, lze spustit pouze startovacím příkazem.')


def _execute_empty_command() -> str:
    """Zpracuje prázdný příkaz, tj. příkaz zadaný jako prázdný řetězec.
    Tento příkaz odstartuje hru, ale v běžící hře se nesmí použít.
    """
    global is_active
    if is_active:
        return 'Prázdný příkaz lze použít pouze pro start hry'
    else:
        is_active = True
        _initialize()
        return ('Vítejte!\n' 
                'Toto je příběh o Červené Karkulce, babičce a vlkovi.\n'
                'Svými příkazy řídíte Karkulku, aby donesla věci babičce.\n'
                'Nebudete-li si vědět rady, zadejte znak ?.')


def _execute_standard_command(command: str) -> str:
    """Připraví parametry pro standardní akci hry,
    tuto akci spustí a vrátí zprávu vrácenou metodou dané akce.
    Byla-li zadána neexistující akce, vrátí oznámení.
    """
    words = command.lower().split()
    action_name = words[0]
    try:
        action  = _NAME_2_ACTION[action_name]
    except KeyError:
        return 'Tento příkaz neznám: ' + action_name
    return action.execute(words)


def _initialize():
    """Inicializuje všechny součásti hry před jejím spuštěním."""
    world.initialize()


############################################################################
class _AAction(world.ANamed, metaclass=ABCMeta):
    """Společná rodičovská třída všech akcí."""

    def __init__(self, name: str, description: str):
        """Zapamatuje si název vytvářené akce a její stručný popis."""
        super().__init__(name)
        self.description = description

    @abstractmethod
    def execute(self, arguments: list[str]) -> str:
        """Realizuje reakci hry na zadání daného příkazu.
        Počet argumentů je závislý na konkrétní akci.
        """


############################################################################
class _End(_AAction):
    """Ukončuje hru a převede ji do pasivního stavu.
    """
    def __init__(self):
        """Jen si u rodiče zapamatuje svůj název a popis."""
        super().__init__("Konec", "Ukončení hry")

    def execute(self, arguments: str) -> str:
        is_active = False
        return 'Ukončili jste hru.\nDěkujeme, že jste si zahráli.'


############################################################################
class _GoTo(_AAction):
    """Přesune hráče do zadaného sousedního prostoru.
    """
    def __init__(self):
        super().__init__("jdi",
                         "Přesune Karkulku do zadaného sousedního prostoru.")

    def execute(self, arguments: list[str]) -> str:
        """Ověří, že zadaný prostor patří mezi sousedy aktuálního
        prostoru, hráče do něj přemístí a vrátí příslušnou zprávu.
        Není-li cílový prostor sousedem, vrátí příslušné oznámení.
        """
        destination_name = arguments[1]
        try:
            destination = world.current_place \
                               .name_2_neighbor[destination_name.lower()]
        except KeyError:
            return ('Do zadaného prostoru se odsud nedá přejít: '
                    + destination_name)
        world.current_place = destination
        return ('Karkulka se přesunula do prostoru:\n' +
                destination.description)


############################################################################
class _Put(_AAction):
    """Přesune h-objekt z košíku do aktuálního prostoru.
    """
    def __init__(self):
        super().__init__('Polož',
                'Přesune zadaný předmět z košíku do aktuálního prostoru.')

    def execute(self, arguments: list[str]) -> str:
        """Ověří existenci zadaného h-objektu v košíku a je-li tam,
        vyjme jej z košíku a přesune do aktuálního prostoru.
        """
        item_name = arguments[1]
        item      = world.BAG.remove_item(item_name)
        if item:
            world.current_place.add_item(item)
            return 'Karkulka vyndala z košíku objekt: ' + item.name
        else:
            return 'Zadaný předmět v košíku není: ' + item_name


############################################################################
class _Take(_AAction):
    """Přesune h-objekt z aktuálního prostoru do košíku.
    """
    def __init__(self):
        super().__init__("Vezmi",
                "Přesune zadaný předmět z aktuálního prostoru do košíku.")

    def execute(self, arguments: list[str]) -> str:
        """Ověří existenci zadaného h-objektu v aktuálním prostoru
        a je-li tam, přesune jej do košíku.
        """
        item_name = arguments[1]
        item      = world.current_place.remove_item(item_name)
        if not item:
            return 'Zadaný předmět v prostoru není: ' + item_name
        world.BAG.add_item(item)
        return 'Karkulka dala do košíku objekt: ' + item.name


############################################################################

# Příznak toho, zda hra právě běží (True), anebo jen čeká na další spuštění
is_active: bool = False     # Na počátku hra čeká, až ji někdo spustí

# Slovník, jehož klíče jsou názvy akcí převedené na malá písmena
# a hodnotami jsou příslušné akce
_NAME_2_ACTION = {'konec': _End(), 'jdi'  : _GoTo(),
                  'polož': _Put(), 'vezmi': _Take(), }



############################################################################
print(f'===== Modul {__name__} ===== STOP')
