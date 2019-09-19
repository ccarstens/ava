from agentspeak import Literal


class Directive:
    def __init__(self, eliciting_utterance, intents=None):
        self.utterance_id = eliciting_utterance
        self.intents = intents if isinstance(intents, list) else [intents]
        self.entities = []

    def has_intents(self):
        return len(self.intents) > 1 or self.intents[0] != "NO_INTENT_DETECTED"

    def add_entity(self, label, value):
        self.entities.append((label, value))

    def entity_to_literal(self, entity: tuple):
        return Literal(entity[0]), entity[1]

    def to_response_belief(self):
        entities = tuple([self.entity_to_literal(entity) for entity in self.entities])

        intent_literal = Literal(self.intents[0])

        arguments = (self.utterance_id, intent_literal, entities)

        return Literal("response", arguments)