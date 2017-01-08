#! ../bin/python

from collections import defaultdict, Sequence
import json
from copy import deepcopy
import itertools

def variable_counter():
	counter = 0
	while True:
		yield counter
		counter += 1

var_count = variable_counter()

class Sentence():
	def __init__(self, operator, *operands):
		self.operator = operator
		self.operands = operands

	def __invert__(self):
		return Sentence("~", self)

	def __and__(self, rhs):
		return Sentence("&", self, rhs)

	def __or__(self, rhs):
		if isinstance(rhs, Sentence):
			return Sentence("|", self, rhs)
		else:
			return PartialSentence(rhs, self)

	def __rand__(self, lhs):
		return Sentence("&", lhs, self)

	def __ror__(self, lhs):
		return Sentence("|", lhs, self)

	def __eq__(self, other):
		return (isinstance(other, Sentence) and self.operator == other.operator and self.operands == other.operands)

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.operator) ^ hash(self.operands)

	def __call__(self, *operands):
		return Sentence(self.operator, operands)

	def __repr__(self):
		operands = [str(operand) for operand in self.operands]
		if is_identifier(self.operator):
			return '{}({})'.format(self.operator, ', '.join(operands)) if operands else self.operator
		elif len(operands) == 1:
			return self.operator + operands[0]
		else:
			return "(" + (" " + str(self.operator) + " ").join(operands) + ")"

def create_elementary_constant(constant):
	return Sentence(constant)

class PartialSentence():
	def __init__(self, operator, lhs):
		self.operator = operator
		self.lhs = lhs

	def __or__(self, rhs):
		return Sentence(self.operator, self.lhs, rhs)

def build_sentence(raw_sentence):
	if isinstance(raw_sentence, str):
		raw_sentence = raw_sentence.replace("=>", "|" + repr("=>") + "|")
		return eval(raw_sentence, namespaceforsentences(create_elementary_constant))

def is_constant_or_predicate(parsed_sentence):
	return isinstance(parsed_sentence, str) and parsed_sentence.isalpha() and parsed_sentence[0].isupper()

def flatten_operands_and_split(operands, operator):
	flattened_operands = []
	for operand in operands:
		if operand.operator == operator:
			flattened_operands += flatten_operands_and_split(operand.operands, operator)
		else:
			flattened_operands.append(operand)
	return flattened_operands

def flatten_and_group_nested_operands(operands, operator):
	flattened_operands = flatten_operands_and_split(operands, operator)
	length = len(operands)
	if length == 0:
		return False
	if length == 1:
		return operands[0]
	else:
		return Sentence(operator, *operands)

def remove_implications(parsed_sentence):
	if is_constant_or_predicate(parsed_sentence.operator) or not parsed_sentence.operands:
		return parsed_sentence
	operands = [remove_implications(operand) for operand in parsed_sentence.operands]
	if parsed_sentence.operator == '=>':
		return ~operands[0] | operands[1]
	else:
		return Sentence(parsed_sentence.operator, *operands)

def move_negation_inwards(sentence):
	if sentence.operator == "~":
		negated_operand = sentence.operands[0]
		if negated_operand.operator == "&":
			operands = [move_negation_inwards(~operand) for operand in negated_operand.operands]
			return flatten_and_group_nested_operands(operands, "|")
		elif negated_operand.operator == "|":
			operands = [move_negation_inwards(~operand) for operand in negated_operand.operands]
			return flatten_and_group_nested_operands(operands, "&")
		elif negated_operand.operator == "~":
			return move_negation_inwards(negated_operand.operands[0])
		return sentence
	elif is_constant_or_predicate(sentence.operator) or not sentence.operands:
		return sentence
	else:
		operands = [move_negation_inwards(operand) for operand in sentence.operands]
		return Sentence(sentence.operator, *operands)

def distribute_and_over_or(sentence):
	if sentence.operator == "&":
		operands = [distribute_and_over_or(operand) for operand in sentence.operands]
		return flatten_and_group_nested_operands(operands, "&")
	elif sentence.operator == "|":
		sentence = flatten_and_group_nested_operands(sentence.operands, "|")
		if sentence.operator != "|":
			return distribute_and_over_or(sentence)
		else:
			length = len(sentence.operands)
			if length == 1:
				return distribute_and_over_or(sentence.operands[0])
			else:
				conjunct = None
				for operand in sentence.operands:
					if operand.operator == "&":
						conjunct = operand
						break
				if conjunct == None:
					return sentence
				else:
					nonconjuncts = []
					for operand in sentence.operands:
						if operand is not conjunct:
							nonconjuncts.append(operand)
					nonconjuncts = flatten_and_group_nested_operands(nonconjuncts, "|")
					result = []
					for conj in conjunct.operands:
						result.append(distribute_and_over_or(conj | nonconjuncts))
					return flatten_and_group_nested_operands(result, "&")
	else:
		return sentence

def is_var_symbol(s):
    return isinstance(s, str) and s[0].isalpha() and s[0].islower()

def is_identifier(s):
	return isinstance(s, str) and s[0].isalpha()

def standardize_variables(sentence, dic = None):
	if dic is None:
		dic = {}
	if not isinstance(sentence, Sentence):
		if isinstance(sentence, tuple):
			return tuple(standardize_variables(operand, dic) for operand in sentence)
		else:
			return sentence
	elif is_var_symbol(sentence.operator):
		if sentence in dic:
			return dic[sentence]
		else:
			v = Sentence('{}{}'.format(sentence.operator, next(var_count)))
			dic[sentence] = v
			return v
	else:
		return Sentence(sentence.operator, *[standardize_variables(a, dic) for a in sentence.operands])

def get_predicates(sentence, negated = False):
	predicates = []
	if isinstance(sentence, Sentence):
		if isinstance(sentence.operator, str) and sentence.operator.isalpha() and sentence.operator[0].isupper() and len(sentence.operands) >= 1:
			predicates.append(sentence.operator if not negated else "~" + sentence.operator)
		else:
			for operand in sentence.operands:
				predicates += get_predicates(operand, True if sentence.operator == "~" else False)
	return predicates

class namespaceforsentences(defaultdict):
	def __missing__(self, key):
		self[key] = result = self.default_factory(key)
		return result

class KnowledgeBase():
	def __init__(self, sentences = None):
		self.sentences = []
		self.index = dict()
		if sentences:
			for sentence in sentences:
				self.tell(sentence)

	def tell(self, sentence):
		self.sentences.append(sentence)
		for predicate in set(get_predicates(sentence)):
			self.add_to_index(predicate, len(self.sentences) - 1)

	def add_to_index(self, predicate, index):
		if predicate in self.index:
			self.index[predicate].add(index)
		else:
			self.index[predicate] = set()
			self.index[predicate].add(index)

	def sentences_containing_predicate(self, predicate):
		sentences = []
		if predicate in self.index:
			for idx in self.index[predicate]:
				sentences.append(self.sentences[idx])
		return set(sentences)

	def sentences_that_resolve_with_sentence(self, sentence):
		sentences_that_resolve = set()
		for predicate in get_predicates(sentence):
			if predicate[0] == "~":
				predicate = predicate[1:]
			else:
				predicate = "~" + predicate
			sentences_that_resolve = sentences_that_resolve.union(self.sentences_containing_predicate(predicate))
		return sentences_that_resolve

	def ask(self, sentence):
		return resolution_refutation(self, sentence)

def is_variable(x):
	return isinstance(x, Sentence) and not x.operands and x.operator[0].islower()

def unify_var(var, x, theta):
	if var in theta:
		return unify(theta[var], x, theta)
	elif x in theta:
		return unify(var, theta[x], theta)
	else:
		substitution = deepcopy(theta)
		substitution[var] = x
		return substitution

def unify(x, y, theta):
	if theta is None:
		return None
	elif x == y:
		return theta
	elif is_variable(x):
		return unify_var(x, y, theta)
	elif is_variable(y):
		return unify_var(y, x, theta)
	elif isinstance(x, Sentence) and isinstance(y, Sentence):
		return unify(x.operands, y.operands, unify(x.operator, y.operator, theta))
	elif isinstance(x, Sequence) and isinstance(y, Sequence):
		if len(x) == len(y) and not isinstance(x, str) and not isinstance(y, str):
			return unify(x[1:], y[1:], unify(x[0], y[0], theta))
		else:
			return None
	else:
		return None

def removeelement(item, seq):
	result = []
	for x in seq:
		if x != item:
			result.append(x)
	return result

def is_variable_symbol(symbol):
	return is_identifier(symbol) and symbol[0].islower()

def substitute(s, x):
	if isinstance(x, list):
		return [substitute(s, xi) for xi in x]
	elif isinstance(x, tuple):
		return tuple([substitute(s, xi) for xi in x])
	elif not isinstance(x, Sentence):
		return x
	elif is_variable_symbol(x.operator):
		return s.get(x, x)
	else:
		return Sentence(x.operator, *[substitute(s, arg) for arg in x.operands])

def resolve(ci, cj):
	new_clauses = []
	clause1_disjuncts = flatten_operands_and_split([ci], "|")
	clause2_disjuncts = flatten_operands_and_split([cj], "|")
	for disjunct1 in clause1_disjuncts:
		for disjunct2 in clause2_disjuncts:
			subst = dict()
			if disjunct1.operator == "~":
				subst = unify(disjunct1.operands[0], disjunct2, subst)
			elif disjunct2.operator == "~":
				subst = unify(disjunct1, disjunct2.operands[0], subst)
			if subst is not None:
				disjunct1 = substitute(subst, disjunct1)
				disjunct2 = substitute(subst, disjunct2)
				if disjunct1 == ~disjunct2 or ~disjunct1 == disjunct2:
					clause1_disjuncts = substitute(subst, clause1_disjuncts)
					clause2_disjuncts = substitute(subst, clause2_disjuncts)
					dnew = list(set(removeelement(disjunct1, clause1_disjuncts) + removeelement(disjunct2, clause2_disjuncts)))
					new_clauses.append(flatten_and_group_nested_operands(dnew, "|"))
	return new_clauses

def resolution_refutation(KB, sentence):
	clauses = KB.sentences + flatten_operands_and_split([standardize_variables(distribute_and_over_or(move_negation_inwards(remove_implications(~build_sentence(sentence)))))], "&")
	NewKB = KnowledgeBase(clauses)
	new = set()
	while True:
		pairs = []
		n = len(NewKB.sentences)
		for i in xrange(n):
			sentences_that_resolve = NewKB.sentences_that_resolve_with_sentence(NewKB.sentences[i])
			for j in xrange(i+1,n):
				if NewKB.sentences[j] in sentences_that_resolve:
					pairs.append((NewKB.sentences[i], NewKB.sentences[j]))
		for (clause1, clause2) in pairs:
			resolvents = resolve(clause1, clause2)
			if False in resolvents:
				return True
			new = new.union(set(resolvents))
		new = remove_duplicates(new)
		if new.issubset(set(NewKB.sentences)):
			return False
		if len(new) + len(NewKB.sentences) > 2000:
			return False
		for c in new:
			if c not in NewKB.sentences:
				NewKB.tell(c)

def remove_duplicates(x):
	n = len(x)
	x = list(x)
	y = []
	sets_to_remove = []
	for i in range(0, n):
		y.append(set(flatten_operands_and_split([x[i]], "|")))
	for i in range(0, n):
		p = set(flatten_operands_and_split([x[i]], "|"))
		for j in range(i + 1, n):
			if p == y[j]:
				sets_to_remove.append(i)
	for index in sorted(set(sets_to_remove), reverse=True):
		del x[index]
	return set(x)

input_file = open("input.txt", "r")

print
queries_count = int(input_file.readline().strip())
print "There are " + str(queries_count) + " queries"

print "The queries are:"
queries = []
for i in xrange(0, queries_count):
	queries.append(input_file.readline().strip())
	print queries[-1]

print
sentences_count = int(input_file.readline().strip())
print "There are " + str(sentences_count) + " sentences"

print "The sentences are:"
sentences = []
for i in xrange(0, sentences_count):
	sentences.append(input_file.readline().strip())
	print sentences[-1]

KB = KnowledgeBase()
print
print "Parsed sentences are:"
for sentence in sentences:
	cnf_sentence = standardize_variables(distribute_and_over_or(move_negation_inwards(remove_implications(build_sentence(sentence)))))
	print "Sentence is: " + sentence
	print "CNF Form is: " + str(cnf_sentence)
	for conjunct in flatten_operands_and_split([cnf_sentence], "&"):
		KB.tell(conjunct)
print
print "Sentences in KB are:"
for sentence in KB.sentences:
	print sentence
print
print "Predicate Index is"
for key in KB.index:
	print "KEY - " + key
	print KB.sentences_containing_predicate(key)

print
print "Sentences and their resolving pairs are:"
for sentence in KB.sentences:
	print "Sentence:"
	print sentence
	print "Resolves with:"
	resolving_sentences = KB.sentences_that_resolve_with_sentence(sentence)
	if resolving_sentences is not None and len(resolving_sentences) > 0:
		for resolving_sentence in resolving_sentences:
			print resolving_sentence
	else:
		print "No sentences will resolve"

print "Start Querying"
output_file = open("output.txt", "w")
for query in queries:
	print "Query: " + query
	decision = KB.ask(query)
	print "Answer: " + str(decision)
	output_file.write(str(decision).upper() + "\n")
output_file.close()