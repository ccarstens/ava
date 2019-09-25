from log import log_nlp as log
from ava.directive import Directive
import agentspeak as asp
from spade_bdi.bdi import get_literal_from_functor_and_arguments
from definitions import *


class NLPController:
    def __init__(self):
        log.debug("init nlpc")

    def process(self, wit_data):
        utterance_id, wit_response = wit_data

        intents = self.extract_intents(wit_response)
        # todo extract named entities
        directive = Directive(utterance_id, intents)
        directive.raw_wit_data = wit_response
        return directive

    def extract_intents(self, wit_dict):
        intent_array = self.keys_exists(wit_dict, "entities", "intent")
        if not intent_array:
            return NO_INTENT_DETECTED
        else:
            return [intent["value"] for intent in intent_array]

    def keys_exists(self, element, *keys):
        '''
        Check if *keys (nested) exists in `element` (dict).
        '''
        if not isinstance(element, dict):
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(keys) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return _element
