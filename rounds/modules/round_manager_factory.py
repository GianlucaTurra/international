from rounds.models import Round
from rounds.modules.generate_round import RoundGenerator, SimpleSwissRoundGenerator
from rounds.modules.save_round import RoundSaver, SimpleSwissRoundSaver
from rounds.schemas import RoundSchema
from tournaments.models import Tournament

from .first_round import FirstRoundGenerator, RandomFirstRoundGenerator


def get_first_round_generator(tournament: Tournament) -> FirstRoundGenerator:
    match tournament.type:
        case Tournament.Types.SIMPLE.value:
            return RandomFirstRoundGenerator(tournament)
    raise Exception("Unsupported Operation")


def get_round_generator(tournament: Tournament) -> RoundGenerator:
    match tournament.type:
        case Tournament.Types.SIMPLE.value:
            return SimpleSwissRoundGenerator(tournament)
    raise Exception("Unsupported Operation")


def get_round_saver(round_input: RoundSchema, current_round: Round) -> RoundSaver:
    match current_round.tournament.type:
        case Tournament.Types.SIMPLE.value:
            return SimpleSwissRoundSaver(round_input, current_round)
    raise Exception("Unsupported Operation")
