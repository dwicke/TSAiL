from util import SaxTerminal
import util

class Grammar(object):
    """docstring for Grammar"""
    def __init__(self):
        super(Grammar, self).__init__()
        self.digram_index = {}
        self.root_production = Rule(self)

    def train_string(self, string):
        """docstring for train_string"""
        input_sequence = [c for c in string]
        if (0 < len(input_sequence)):
            self.root_production.last().insert_after(Symbol.factory(self, input_sequence.pop(0)))
        while (0 < len(input_sequence)):
            # get the last rule and insert the symbol at the end
            self.root_production.last().insert_after(Symbol.factory(self, input_sequence.pop(0)))
            # now check to see if this digram exists
            match = self.get_index(self.root_production.last().prev)
            if not match: ## if it doesn't exist
                print("Not matched so adding to index {}".format(self.root_production.last().prev.value()))
                self.add_index(self.root_production.last().prev)
            elif match.next != self.root_production.last().prev: ## if the next isn't the same as the prev
                self.root_production.last().prev.process_match(match)

    def add_index(self, digram):
        """docstring for index"""
        self.digram_index[digram.hash_value()] = digram

    def get_index(self, digram):
        """docstring for get"""
        return self.digram_index.get(digram.hash_value())

    def clear_index(self, digram):
        """docstring for clear_index"""
        if self.digram_index.get(digram.hash_value()) == digram:
            self.digram_index[digram.hash_value()] = None

    def print_grammar(self):
        """docstring for print_grammar"""
        output_array = []
        rule_set = [self.root_production]
    
        i = 0
        for rule in rule_set:
            output_array.append("%s --(%d)--> " % (i, rule.reference_count))
            line_length = rule.print_rule(rule_set, output_array, len("%s --(%d)--> " % (i, rule.reference_count)))
        
            if i > 0:
                output_array.append(' ' * (57 - line_length))
                line_length = rule.print_rule_expansion(rule_set, output_array, line_length)
            output_array.append('\n');
            i += 1

        return "".join([str(x) for x in output_array])

    def getRules(self):
        theRules = []
        output_array = []
        rule_set = [self.root_production]
    
        i = 0
        for rule in rule_set:
            output_array = []
            line_length = rule.print_rule(rule_set, output_array, 0)
            beforeExpansion = output_array
            output_array = []
            if i > 0:
                line_length = rule.print_rule_expansion(rule_set, output_array, 0)
            theRules.append(util.Rule(i, rule.reference_count, beforeExpansion, output_array, rule.positions))
            i += 1
        return theRules


class Rule(object):
    
    unique_rule_number = 1
    
    def __init__(self, grammar):
        super(Rule, self).__init__()
        self.guard = Symbol.guard(grammar, self)
        self.guard.join(self.guard)
        self.reference_count = 0
        self.unique_number = Rule.unique_rule_number
        self.positions = []
        Rule.unique_rule_number += 1
    
    def first(self): return self.guard.next

    def last(self): return self.guard.prev

    def increment_reference_count(self): self.reference_count += 1

    def decrement_reference_count(self): self.reference_count -= 1

    def add_position(self, pos): 
        self.positions.append(pos)

    def print_rule(self, rule_set, output_array, line_length):
        """docstring for print_rule"""
        symbol = self.first()
        while not symbol.is_guard():
            line_length = symbol.print_rule(rule_set, output_array, line_length)
            symbol = symbol.next
        return line_length

    def print_rule_expansion(self, rule_set, output_array, line_length):
        """docstring for print_rule_expansion"""
        symbol = self.first()
        while not symbol.is_guard():
            line_length = symbol.print_rule_expansion(rule_set, output_array, line_length)
            symbol = symbol.next
        return line_length


class Symbol(object):
    """docstring for Symbol"""
    def __init__(self, grammar):
        """docstring for __init__"""
        self.grammar = grammar
        self.next = None
        self.prev = None
        self.originalPosition = None

    def print_terminal(self):
        """docstring for print_terminal"""
        if (' ' == self.value()):
            return '_'
        else:
            return self.value()

    def print_rule_expansion(self, _, output_array, line_length):
        """docstring for print_rule_expansion"""
        output_array.append(self.print_terminal())
        return line_length + len(self.print_terminal())

    def print_rule(self, _, output_array, line_length):
        """docstring for print_rule"""
        output_array.append("%s " % self.print_terminal())
        return line_length + len("%s " % self.print_terminal())

    @staticmethod
    def factory(grammar, value):
        """docstring for factory"""
        if (SaxTerminal == type(value)):
            return Terminal(grammar, value, value.getID())
        elif (Terminal == type(value)):
            return Terminal(grammar, value.terminal, value.terminal.getID())
        elif (NonTerminal == type(value)):
            return NonTerminal(grammar, value.rule)
        elif (Rule == type(value)):
            return NonTerminal(grammar, value)
        else:
            raise "type(value) == %s" % type(value)
    
    @staticmethod
    def guard(grammar, value):
        """docstring for guard"""
        return Guard(grammar, value)

    def join(self, right):
        """
        Links two symbols together, removing any old digram from the hash table.
        """
        if (self.next):
            self.delete_digram()
            
            """
            This is to deal with triples, where we only record the second
            pair of overlapping digrams. When we delete the second pair,
            we insert the first pair into the hash table so that we don't
            forget about it. e.g. abbbabcbb
            """
            ## TSAT doesn't do this:
            if ((right.prev is not None) and (right.next is not None) and
                right.value() == right.prev.value() and
                right.value() == right.next.value()):
                self.grammar.add_index(right)
            if ((self.prev is not None) and (self.next is not None) and
                self.value() == self.next.value() and
                self.value() == self.prev.value()):
                self.grammar.add_index(self)
        self.next = right
        right.prev = self

    def delete_digram(self):
        """Removes the digram from the hash table"""
        if (self.is_guard() or self.next.is_guard()):
            pass
        else:
            self.grammar.clear_index(self)

    def insert_after(self, symbol):
        """Inserts a symbol after this one"""
        symbol.join(self.next)
        self.join(symbol)

    def is_guard(self): return False # Overridden by Guard class

    def expand(self):
        """
        This symbol is the last reference to its rule. It is deleted, and the
        contents of the rule substituted in its place.
        """
        left = self.prev
        right = self.next
        first = self.rule.first()
        last = self.rule.last()
        
        self.grammar.clear_index(self)
        left.join(first)
        last.join(right)
        self.grammar.add_index(last)

    def propagate_change(self):
        """docstring for propagate_change"""
        if self.is_guard() or self.next.is_guard():
            if (self.next.is_guard() or self.next.next.is_guard()):
                return
            match = self.grammar.get_index(self.next)
            if not match:
                self.grammar.add_index(self.next)
            elif match.next != self.next:
                self.next.process_match(match)
        else:
            match = self.grammar.get_index(self)
            if not match:
                self.grammar.add_index(self)
                if (self.next.is_guard() or self.next.next.is_guard()):
                    return
                match = self.grammar.get_index(self.next)
                if not match:
                    self.grammar.add_index(self.next)
                elif match.next != self.next:
                    self.next.process_match(match)
            elif match.next != self:
                self.process_match(match)

    def substitute(self, rule):
        """Replace a digram with a non-terminal"""
        prev = self.prev
        prev.next.delete()
        prev.next.delete()
        rule.add_position(self.originalPosition)
        nonterm = Symbol.factory(self.grammar, rule)
        nonterm.originalPosition = self.originalPosition
        prev.insert_after(nonterm)

    def process_match(self, match):
        """Deal with a matching digram"""
        rule = None
        if (match.prev.is_guard() and match.next.next.is_guard()):
            # reuse an existing rule
            rule = match.prev.rule
            self.substitute(rule)
            self.prev.propagate_change()
        else:
            # create a new rule
            rule = Rule(self.grammar)
            rule.last().insert_after(Symbol.factory(self.grammar, self))
            rule.last().insert_after(Symbol.factory(self.grammar, self.next))
            self.grammar.add_index(rule.first())
            
            match.substitute(rule)
            match.prev.propagate_change()
            self.substitute(rule)
            self.prev.propagate_change()

        # Check for an under-used rule
        if (NonTerminal == type(rule.first()) and (rule.first().rule.reference_count == 1)):
            rule.first().expand()
    
    def value(self):
        """docstring for value"""
        return (self.rule.unique_number if self.rule else self.terminal)

    def string_value(self):
        """docstring for string_value"""
        if self.rule:
            return "rule: %d" % self.rule.unique_number
        else:
            return self.terminal

    def hash_value(self):
        """docstring for hash_value"""
        return "%s+%s" % (self.string_value(), self.next.string_value())


class Terminal(Symbol):
    """docstring for Terminal"""
    def __init__(self, grammar, terminal, pos):
        super(Terminal, self).__init__(grammar)
        self.terminal = terminal
        self.originalPosition = pos
        
    def value(self):
        """docstring for value"""
        return self.terminal
    
    string_value = value

    def delete(self):
        """
        Cleans up for symbol deletion: removes hash table entry and decrements
        rule reference count.
        """
        self.prev.join(self.next)
        self.delete_digram()


class NonTerminal(Symbol):
    """docstring for NonTerminal"""
    def __init__(self, grammar, rule):
        super(NonTerminal, self).__init__(grammar)
        self.rule = rule
        self.rule.increment_reference_count()

    def value(self):
        """docstring for value"""
        return self.rule.unique_number

    def string_value(self):
        """docstring for string_value"""
        return "rule: %d" % self.rule.unique_number

    def print_rule(self, rule_set, output_array, line_length):
        """docstring for print_rule"""
        if (self.rule in rule_set):
            rule_index = rule_set.index(self.rule)
        else:
            rule_index = len(rule_set)
            rule_set.append(self.rule)
        output_array.append("%d " % rule_index)
        return line_length + len("%d " % rule_index)

    def print_rule_expansion(self, rule_set, output_array, line_length):
        """docstring for print_rule_expansion"""
        return self.rule.print_rule_expansion(rule_set, output_array, line_length)

    def delete(self):
        """
        Cleans up for symbol deletion: removes hash table entry and decrements
        rule reference count.
        """
        self.prev.join(self.next)
        self.delete_digram()
        self.rule.decrement_reference_count()

class Guard(Symbol):
    """
    The guard symbol in the linked list of symbols that make up the rule.
    It points forward to the first symbol in the rule, and backwards to the last
    symbol in the rule. Its own value points to the rule data structure, so that
    symbols can find out which rule they're in.
    """

    def __init__(self, grammar, rule):
        super(Guard, self).__init__(grammar)
        self.rule = rule

    def is_guard(self): return True

    def value(self):
        """docstring for value"""
        return self.rule.unique_number

    def string_value(self):
        """docstring for string_value"""
        return "rule: %d" % self.rule.unique_number

    def delete(self):
        """
        Cleans up for symbol deletion: removes hash table entry and decrements
        rule reference count.
        """
        self.prev.join(self.next)
