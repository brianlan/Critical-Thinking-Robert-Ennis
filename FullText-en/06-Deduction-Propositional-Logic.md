# CHAPTER 6 Deduction: Propositional Logic


Now that you understand deductive validity and have some techniques for handling class logic, you are ready to move on to propositional logic. Here are three examples of propositional-logic arguments.

#### Example 6:1
a. If *Ben is a cat*, then *Ben is an animal*.
b. *Ben is not an animal*.
c. Therefore, *Ben is not a cat*.

#### Example 6:2
a. Either *Arlene stabbed Al*, or *Arlene is innocent*.
b. *Arlene did not stab Al*.
c. Therefore, *Arlene is innocent*.

#### Example 6:3
If *parking is prohibited on this street* and *Sybil parked there last night*, then *Sybil is in trouble*. However, I know that *Sybil is not in trouble* and that *parking is prohibited on this street*. Therefore, *she did not park there last night*.

You can probably see that the first two arguments are deductively valid, but you might not be sure about the third. In any case, circle techniques do not work here, so we will move on to another common set of techniques. As with class logic, there are many strategies and refinements that will be omitted. But basic ideas will be presented, ideas that you can build on by yourself, or through reading other sources.[^1]

[^1]: Most standard elementary deductive logic texts would be helpful. For one that continues an emphasis on natural language, see my *Natural Language Logic*, forthcoming.

## Propositions

According to the meaning of *proposition* that we shall use, a *proposition*, roughly speaking, is either a sentence or, if embedded in a more complex sentence, could be a sentence if isolated.[^2] It is a set of concepts (or words) with a given meaning that can stand alone and make sense if asserted. Here are some examples of simple propositions that appear in italics in Examples 6:1, 6:2, and 6:3:

#### Example 6:4: Some Basic Propositions
a. Ben is a cat.
b. Ben is an animal.
c. Ben is not an animal.
d. Ben is not a cat.
e. Arlene stabbed Al.
f. Arlene is innocent.
g. Arlene did not stab Al.
h. Parking is prohibited on this street.
i. Sybil parked there last night.
j. Sybil is in trouble.
k. Sybil is not in trouble.
l. She did not park there last night.

Look again at the arguments in Examples 6:1, 6:2, and 6:3 to see the role that the propositions in Example 6:4 play in those arguments. Note also the role in Examples 6:1, 6:2, and 6:3 played by the words *if, then, either, or, and and*.

Here are some things that are not propositions because they cannot stand alone and make sense if asserted:

#### Example 6:5
a. Robins
b. People under eighteen
c. anybody is under eighteen (in "If *anybody is under eighteen*, then that person may not enter.")

The classes that are *a* and *b* in Example 6:5 obviously do not make sense to assert all by themselves. Suppose, for example, someone came up to you and said, "Robins." What sense would you make of that? Of course it would make sense as an answer to a question, such as "What kinds of birds are those?" But then the speaker would implicitly be asserting a complete proposition, *Those are robins*, which can stand alone and make sense if asserted. But the word *Robins*, without any such implication, is not an assertion.

[^2]: A more precise, theoretical definition of *proposition* would not be helpful for present purposes.

Even though Example 6:5c (*anybody is under eighteen*) has a subject and predicate, someone's trying to assert it does not make sense, if its words mean what they mean in the complete sentence given in parentheses in that example. What would you make of someone's coming up to you and saying, "Anybody is under eighteen," in the sense in which it is meant in Example 6:5c? Actually, the proposition in quotes in Example 6:5c fits best under class logic because its meaning is *People under eighteen may not enter*.

## If-Then Reasoning
Reasoning with *if-then* propositions is the most important kind of propositional reasoning, so we shall start with it. The following argument is a case of *if-then* reasoning because it employs an *if-then* proposition:

a. If Ben is a cat, then Ben is an animal.
b. Ben is a cat.
c. Therefore, Ben is an animal.

The first reason, *a*, is an *if-then* proposition consisting of two shorter propositions joined by the words, *if* and *then*, in appropriate places. The second reason, *b*, is a separate assertion of the *if* part. The conclusion, *c*, is an assertion of the *then* part of *a*.
The first (the complex) proposition asserts that the second reason is enough to entitle us to draw the conclusion. The conclusion follows necessarily from the two reasons together.
This is not to say that the conclusion is true. It might very well be that Ben is not an animal. But if the reasons are true, then he must be an animal. That is, given that it is true that if Ben is a cat, then Ben is an animal, and given also that Ben is a cat, then Ben must be an animal. If those two reasons are true, there is no way to avoid the conclusion. Therefore, the argument in Example 6:6 is deductively valid.

### Affirming the Antecedent
In Example 6:6, the *if* proposition has been affirmed (in *b*). This entitles us to draw as a conclusion the *then* proposition (*c*). Because the *if* part is called the *antecedent* and because the antecedent is separately affirmed (in reason *b*), the form of reasoning in Example 6:6 is called *affirming the antecedent*. Affirming the antecedent is a deductively valid form.

### Antecedents and Consequents
In the first reason (*a*) of Example 6:6, the proposition *Ben is an animal* is the *then* part of the *if-then* proposition. The *then* part of an *if-then* proposition is called the *consequent*. In the first reason of Example 6:6, *Ben is an animal* is the consequent.
Before going on to look at other forms of reasoning, let us pause to identify antecedents and consequents. The antecedent often comes first, but it does not always do so. Sometimes the antecedent comes second and the consequent comes first (Example 6:7a), and sometimes the antecedent is inserted between parts of the consequent (Example 6:7b):

**Example 6:7**
a. Ben is an animal if Ben is a cat.
b. Sybil, if parking is prohibited on this street, is in trouble.

Examples 6:6a and 6:7a mean the same thing, even though the order is reversed. This is because the word *if* is attached to the same proposition (*Ben is a cat*) in both cases. The total *if-then* proposition, whatever the order (as long as *if* stays with *Ben is a cat*), tells us that Ben's being a cat is sufficient to establish that Ben is an animal.

Note that the word *if* is not part of the antecedent; rather it is an indicator of the antecedent. The antecedent is the proposition coming right after the word *if*. The consequent is the other unit of the complex proposition. The word *then*, if it is used, is *not* part of the consequent. When it appears, it is an *indicator* of the consequent. In Example 6:7, the word *then* was omitted, as it always is when the consequent comes first. Sometimes it is omitted even when the consequent comes second, as in *If Ben is a cat, Ben is an animal*. The word *then* is not really needed in front of the consequent (*Ben is an animal*) to make the complex proposition read smoothly. However, it can be there, as in reason *a* in Example 6:6.

Another difference that we can usually ignore comes from the substituting of a pronoun or some similar term to refer to something already named. Hence (assuming that Ben is male) the *if-then* propositions in Example 6:8 are essentially the same in meaning for our purposes:

**Example 6:8**
a. If Ben is a cat, then Ben is an animal.
b. If Ben is a cat, then he is an animal.

## Summary
Propositions can stand alone and make sense when asserted. When two propositions are appropriately joined together by the words *if* and *then* (although *then* is not always needed), the result is a more complex *if-then* proposition). The *if* part is the *antecedent*. The *then* part is the *consequent*. Although the antecedent usually comes first, the consequent sometimes comes first, and sometimes the antecedent comes between parts of the consequent. The substitution of a pronoun, when referring to something already named, generally does not change the meaning of an *if-then* proposition. When an argument consists of an *if-then* proposition as one reason, the affirmed antecedent as the other reason, and the consequent by itself as the conclusion, this argument is of the form, *affirming the antecedent*, a deductively valid form of argument.

## Check-Up 6A

**True or False?**  
If a statement is false, change a crucial word or words to make it true.

6:1 The *if* proposition in an *if-then* proposition is called the *antecedent*.  
6:2 The *then* proposition in an *if-then* proposition is called the *consequent*, but only when the word *then* is actually there.  
6:3 The following two complex propositions mean the same thing:
    a. If John is in school, then Mary is happy.
    b. Mary is happy, if John is in school.
6:4 In the following two complex propositions, the antecedent is the same:
    a. Karl was depressed, if he lost the election.
    b. Karl lost the election, if he was depressed.
6:5 Propositions can stand alone, and do make sense if asserted.  
6:6 *Tom is a turtle* is a proposition.  
6:7 The proposition that comes first in an *if-then* proposition is called the *antecedent*.  
6:8 The following argument is of the form, affirming the antecedent, and is deductively valid:
    a. Tom is slow, if Tom is a turtle.
    b. Tom is slow.
    c. Therefore, Tom is a turtle.

### Short Answer
For each of the following items, (a) underline the antecedent once and (b) underline the consequent twice, but do not underline *if* and *then* because they are not in these examples part of the antecedent and consequent. The first two are done as examples. If your instructor has not made another suggestion, either photocopy these pages or copy the items.

6:9 If Tom is a turtle, then Tom is slow.  
6:10 Tom is slow, if Tom is a turtle.  
6:11 If junipers are poisonous, then the cattle are in danger.  
6:12 The cattle are in danger, if junipers are poisonous.  
6:13 If the supervisor forgot about us, then there is a shortage of concrete.  
6:14 If Terry got into the Blue Room, then she lied about her age.

6:15 If Terry lied about her age, then she got into the Blue Room.
6:16 If Arlene is a liberal, then she supported the prime minister.
6:17 Joanna, if she supported the prime minister, is a liberal.
6:18 If Arlene admitted that she did it, then she did it.
6:19 Martin thinks, if he is wearing a red hat, that hunters might be around.
6:20 Arlene, if she admitted that she did it, did it.
6:21 If she killed him, then she performed the act that caused his death.
6:22 She killed him, if she performed the act that caused his death.
6:23 If the blood is Al's blood, then it is type A.
6:24 The blood, if it is type A, is Al's blood.
6:25 Tom Jeffers, if he was seen in the hospital waiting room between 10 P.M. and midnight, did not do it.
6:26 If Tom Jeffers was seen in the hospital waiting room between 10 P.M. and midnight, then he did not do it.

## Affirming and Denying the Antecedent and Consequent

In addition to affirming the antecedent, there are three other basic moves one can make from an *if-then* proposition. Two are deductively invalid, and one is deductively valid. Example 6:9 is an illustration of the move called *denying the antecedent*, so called because one of the reasons denies the antecedent of the other reason.

**Example 6:9**
a. If Ben is a cat, then Ben is an animal.
b. Ben is not a cat.
c. Therefore, Ben is not an animal.

Reason *b* denies the antecedent of reason *a* and the conclusion does not necessarily follow. Even if the reasons are true, it would still be possible for Ben to be an animal. He might be a goat, for example. Denying the antecedent is a deductively invalid form.

Another deductively invalid form is *affirming the consequent*, so called because one reason affirms the consequent of the other reason, as in Example 6:10:

**Example 6:10**
a. If Ben is a cat, then Ben is an animal.
b. Ben is an animal.
c. Therefore, Ben is a cat.

Reason *b* affirms the consequent of reason *a*. Again, the conclusion does not necessarily follow. The reasons allow that Ben could be some other kind of animal than a cat, even though his being a cat would ensure his being an animal. Affirming the consequent is a deductively invalid form.

The last basic form in this series is called *denying the consequent* because one reason denies the consequent of the other reason, as in Example 6:11:

**Example 6:11**
a. If Ben is a cat, then Ben is an animal.
b. Ben is not an animal.
c. Therefore, Ben is not a cat.

Reason *b* denies the consequent of reason *a*. This time, the conclusion necessarily follows. If you do not see this, consider: Assuming that the reasons are true, suppose, contrary to the conclusion, that Ben *were* a cat. Then according to reason *a*, Ben would have to be an animal. But reason *b* says that he is not an animal. So, he cannot be a cat. Denying the consequent is a deductively valid form.

## Summary So Far

This chapter so far has further explored the *I* in *FRISCO* by elaborating some basic features of propositional logic, a kind of deductive logic that is in some ways similar to class logic. In propositional logic, the basic building block is the proposition, which consists of a subject and predicate, and can stand alone and meaningfully be asserted.

The most important propositional-logic relationship is implication, as found in *if–then* propositions that connect an antecedent (the *if* part) with a consequent (the *then* part). Each of these is itself a proposition.
- An *if–then* proposition says that the truth of the antecedent proposition is enough to establish the truth of the consequent proposition. It says that the consequent must be true in order that the antecedent be true. That is, unless the consequent is true, the antecedent cannot be true. But a standard *if–then* proposition does *not* say that the truth of the consequent is enough to establish the truth of the antecedent, nor does it say that the antecedent must be true in order that the consequent be true. It is a common deductive error to think that an *if–then* proposition says these things.

*Affirming the antecedent* and *denying the consequent* are deductively valid moves. *Affirming the consequent* and *denying the antecedent* are deductively invalid moves.

Table 6.1 summarizes the relationships among affirming and denying antecedents and consequents. Do not memorize it. Just think about its parts until you are sure that you feel comfortable with what it says in terms of your own examples.



**TABLE 6.1 Deductive validity of the Four Basic Forms of "If-Then" Reasoning**
| | Antecedent | Consequent |
| --- | --- | --- |
| Affirming | Deductively Valid | Deductively Invalid |
| Denying | Deductively Invalid | Deductively Valid |

## Check-Up 6B
**True or False?**
If a statement is false, change a crucial word or words to make it true.

6:27 *Affirming the antecedent* is a deductively valid form.
6:28 *Denying the antecedent* is a deductively invalid form.
6:29 The following is a case of denying the consequent:
  a. If Marguerite is here, then Estelle is happy.
  b. Estelle is not happy.
  c. Therefore, Marguerite is not here.
6:30 *Denying the consequent* is a deductively invalid form.
6:31 *Affirming the consequent* is a deductively invalid form.

### Short Answer
For each of the following items, indicate the form of the argument, using the following abbreviations: For *affirming the antecedent*, use *AA*; for *denying the antecedent*, use *DA*; for *affirming the consequent*, use *AC*; and for *denying the consequent*, use *DC*. Also indicate whether the argument is deductively valid (DV) or deductively invalid (DI). The first one is done as an example.

6:32 a. If Marguerite is here, then Estelle is happy.
  b. Estelle is happy.
  c. Therefore, Marguerite is here. AC, DI
6:33 a. If Joanna supported the prime minister, then she is a liberal.
  b. Joanna is not a liberal.
  c. Therefore, Joanna did not support the prime minister.
6:34 a. If Joanna supported the prime minister, then she is a liberal.
  b. Joanna is a liberal.
  c. Therefore, Joanna supported the prime minister.
6:35 a. If Joanna is a liberal, then she supported the prime minister.
  b. Joanna did not support the prime minister.
  c. Therefore, Joanna is not a liberal.
6:36 a. Terry, if she lied about her age, got into the Blue Room.
  b. Terry got into the Blue Room.
  c. Therefore, Terry lied about her age.
  
6:37
a. Terry lied about her age, if she got into the Blue Room.
b. Terry did not get into the Blue Room.
c. Therefore, she did not lie about her age.

6:38
a. The blood is type A.
b. The blood is type A, if it is Al's.
c. Therefore, the blood is Al's.

6:39
a. If junipers are poisonous, then the cattle are in danger.
b. The cattle are in danger.
c. Therefore, junipers are poisonous.

6:40
a. Arlene, if she admitted that she did it, did it.
b. Arlene did not do it.
c. Therefore, Arlene did not admit that she did it.

6:41
a. Arlene admitted that she did it.
b. If Arlene admitted that she did it, then she did it.
c. Therefore, Arlene did it.

### Conversion
Exchanging the antecedent and consequent is a significant change. That is, the two statements in Example 6:12 (*a* and *b*) are very different from each other.

#### Example 6:12
a. If Ben is a cat, then Ben is an animal.
b. If Ben is an animal, then Ben is a cat.

In Example 6:12*b*, the word *if* is attached to (that is, it comes just before) the proposition *Ben is an animal*. That makes *Ben is an animal* the antecedent, instead of *Ben is a cat*, and radically changes the meaning of the whole *if-then* proposition. The new *if-then* proposition (Example 6:12*b*) asserts that Ben's being an animal is sufficient to establish that Ben is a cat. This clearly is not what the original asserted. The original asserted that Ben's being a cat was sufficient to establish that Ben is an animal.

The distinction between the antecedent and the consequent is the most important distinction in *if-then* propositional logic. Many of the mistakes people make in propositional logic can be roughly characterized as getting this distinction confused, although usually in more complex circumstances.

Exchanging these two different ways of joining the elementary propositions in *if-then* propositions is common enough to have a name: *conversion*. To *convert* an *if-then* proposition is to exchange the antecedent and the consequent. Example 6:12*b* is the converse of Example 6:12*a* and Example 6:12*a* is the converse of 6:12*b*.

The location of the antecedent and consequent with respect to each other has no bearing on whether they have been exchanged. All that matters is the location of the word *if*. Hence, the two propositions in Example 6:13 are also converses of each other:

#### Example 6:13
a. Ben is an animal if Ben is a cat.
b. If Ben is an animal, Ben is a cat.

Conversion is a deductively invalid form. It is also usually a mistake (that is, invalid in the everyday meaning of *invalid*).

### Contraposition
A *contrapositive* of a proposition is the proposition with the antecedent and consequent exchanged and each denied. In Example 6:14, *b* is the contrapositive of *a*.

#### Example 6:14
a. If Ben is a cat, then Ben is an animal.
b. Therefore, if Ben is not an animal, Ben is not a cat.

Ordinarily, contrapositives can be substituted for each other in arguments.
The move from *a* to *b* in Example 6:14 is called contraposition: The antecedent and consequent were exchanged and each was denied (or negated). More precisely, the exchange calls for shifting the *if* from one proposition to the other, accompanied by the denial of each. The conclusion (*b*) follows from the reason (*a*) by the same kind of thinking that shows denying the consequent to be deductively valid: Example 6:14*a* tells us that if Ben is a cat, then Ben is an animal. Granting that, let us suppose that Ben is not an animal. Then we would have to conclude that Ben is not a cat. Otherwise, he would be an animal (from *a*). So, if Ben is not an animal, then Ben is not a cat. This *if-then* proposition is our conclusion (6:14*b*). Contraposition is a deductively valid form.[^3]

## Negation
To negate the proposition *Ben is a cat* is to assert that Ben is not a cat. Generally speaking, one negates by introducing such words or prefixes as *not*, *non-*, *no*, *un-*, and *it is not the case that*. The three propositions in Example 6:15 are negations (or denials) of the proposition *Ben is a cat* and are propositions themselves. For present purposes, they are essentially equivalent to each other:

#### Example 6:15
a. Ben is not a cat.
b. It is not true that Ben is a cat.
c. Ben is a non-cat.

[^3]: Beware of contraposing *if-then* propositions that express causal connections. Make sure that the contrapositive is stated so that it makes sense in the situation.

Example 6:15a is the more convenient way to express the thought.

### Double Negation
The standard double negation rule is this: *Two negatives make a positive*. That is, two negatives cancel each other out. Following this rule, the propositions in Example 6:16 are basically equivalent to each other:

**Example 6:16**
a. Ben is a cat.
b. It is false that Ben is not a cat.
c. It is not true that Ben is not a cat.
d. It is not the case that Ben is a non-cat.

The last three (*b*, *c*, and *d*) contain double negations. The double negations cancel each other out to make the positive proposition *Ben is a cat*. Think about the meaning of each of these to make sure you understand why each of the last three contains a double negation, and why each means the same as the first.

But a problem can arise when handling some double negations. Suppose, for example, someone says that it has not been proved that the apple trees are not productive. The person who says this might be holding that the trees are midway between being unproductive and productive, or that even though they might well be unproductive, it simply has not been proved. In such a case, it would be misleading simply to eliminate the double negative and conclude that it has been proved that the apple trees are productive. Therefore, you should keep an amendment to the rule in the back of your mind: *Two negatives make a positive, unless some middle ground is possible*.

The double-negation rule is more difficult to use with this amendment, but that is the way things are. The language and its users are sometimes very subtle and sometimes very plain. You must judge a situation for what it is.

### Double Negation and Contraposition
Sometimes when you make the contrapositive of a proposition you produce a double negation, which usually can then be eliminated.

**Example 6:17**
a. If Ben is a cat, then Ben is not a dog.
b. If it is false that Ben is not a dog, then Ben is not a cat.
c. If Ben is a dog, then Ben is not a cat.

In Example 6:17, the move from *a* to *b* is contraposition. The move from *b* to *c* is the elimination of a double negative in the antecedent of *b*.

Eliminating double negatives makes things easier to understand, but it must be done with caution, and sometimes must not be done (as you saw in the previous section).

## Summary
The converse of an *if-then* proposition is formed by exchanging the antecedent and the consequent so that the antecedent becomes the consequent, and vice versa. Conversion is a deductively invalid move.

The contrapositive of an *if-then* proposition is formed by exchanging and negating the antecedent and the consequent. Contraposition is a deductively valid move.

Double negatives can be dropped, unless there is a middle ground. Beware.

## Check-Up 6C
**True or False?**
If a statement is false, change a crucial word or words to make it true.

6:42 Conversion is deductively invalid.
6:43 *We are short of concrete if the supervisor forgot about us* is the converse of *If the supervisor forgot about us, we are short of concrete*.
6:44 *If we are short of concrete, then the supervisor forgot about us* is the converse of *We are short of concrete if the supervisor forgot about us*.
6:45 Exchanging the antecedent and consequent, while moving the word *if* to the other clause, is called *conversion* and is generally a mistake.
6:46 To make a contrapositive, you exchange the antecedent and consequent so that the antecedent becomes the consequent and the consequent becomes the antecedent, and then you separately deny each.
6:47 Contraposition is deductively valid.
6:48 Two negatives always make a positive, enabling us to drop every pair of negatives in a proposition.
6:49 The following two *if-then* propositions are contrapositives of each other and therefore imply each other:
a. If Tom is a turtle, then Tom is slow.
b. If Tom is not slow, then Tom is not a turtle.
6:50 The following two *if-then* propositions are contrapositives of each other and therefore imply each other:
a. It is type A, if it is Al's blood.
b. If it is not type A, then it is not Al's blood.
6:51 The following two *if-then* propositions are contrapositives of each other and therefore imply each other:
a. Tom Jeffers did not do it, if he was seen in the hospital waiting room between 10 P.M. and midnight.
b. If Tom Jeffers was not seen in the hospital waiting room between 10 P.M. and midnight, then he did it.

6:52 The second of these two *if-then* propositions is a useful simplification of the first:
a. Joanna is not a liberal, if it is not true that she did not support the prime minister.
b. If Joanna supported the prime minister, then she is not a liberal.

### Short Answer
For each of the following, on a separate sheet of paper, fill in an appropriate word or words in the second proposition so that it means the same as the first (or write only the words *if* and *then* in the proper order). Capitalize a letter if necessary. Avoid conversion. The first is done as an example.

6:53 a. Our cattle are in danger, if junipers are poisonous.
b. *If junipers are poisonous, then* our cattle are in danger.

6:54 a. If Joanna supported the prime minister, then she is a liberal.
b. ____ Joanna is a liberal, ____ she supported the prime minister.

6:55 a. Arlene did it, if she admitted that she did it.
b. ____ Arlene admitted that she did it, ____ Arlene did it.

6:56 a. The blood, if it is Al's blood, is type A.
b. ____ the blood is Al's blood, ____ it is type A.

6:57 a. This vehicle, if it has a motor, is prohibited.
b. ____ this vehicle has a motor, ____ the vehicle is prohibited.

### More Short Answer
Simplify the following by eliminating the double negatives. If you do not think that the double negative can be eliminated because the simple rule ("Two negatives make a positive") does not apply, then say that the double negative may not be eliminated. The first is done as an example. Use a separate sheet of paper.

6:58 It is not true that John is not here. *Result:* John is here.
6:59 It is false that motorcycles are not permitted.
6:60 It is not true that the diamond is not in the queen's crown.
6:61 There is no doubt that she is not guilty.
6:62 If Arlene did it, then it is not true that she did not admit that she did it.
6:63 It is not true that our cattle are not healthy, if they did not eat the junipers.
6:64 If the pork we had tonight was not inexpensive, then our budget will be exceeded.
6:65 If a majority approved the resolution, then the society will not meet in a state that has not passed the proposed constitutional amendment.
6:66 If Arlene did not do it, then she did not admit doing it.

### More Short Answer
Write a contrapositive of each of the following propositions. Simplify, if a double negative can be eliminated without changing the meaning.

6:67 If Arlene admitted it, then she did it.
6:68 If junipers are poisonous, then our cattle are ill.
6:69 The blood is type A, if it is Al's blood.
6:70 If a vehicle has a motor, then the vehicle is prohibited.
6:71 If Sara Lee did not lie about her age, then she was not admitted to the Panama Club.
6:72 If the supervisor did not forget about us, then we have enough concrete.
6:73 Martin, if he is wearing a red hat, thinks that hunters might be around.
6:74 If the gift is inexpensive, then Shiboen bought it.
6:75 If she was convicted, then the jury was convinced beyond a reasonable doubt that the three conditions for murder were satisfied.
6:76 The battery is in bad condition, if you left the lights on all night.
6:77 If a majority approved the resolution, then the society did not meet in a state that has not passed the proposed constitutional amendment.

### More Short Answer
For each of the following arguments, state the final conclusion. Then decide whether each is deductively valid, indicating your reasons in abbreviated form. For these items, choose your reasons from the following list:

| Justifications of a judgment of deductive validity (DV): | Justifications of a judgment of deductive invalidity (DI): |
| --- | --- |
| Affirming the Antecedent (AA) | Denying the Antecedent (DA) |
| Denying the Consequent (DC) | Affirming the Consequent (AC) |
| Contraposition (CONTR) | Conversion (CONV) |
| Eliminable Double Negation (EDN) | Noneliminable Double Negation (NDN) |

For some items, you will need to break the argument into parts and deal with each part separately, giving more than one justification. If any part of the argument is deductively invalid, the whole argument is deductively invalid. The first two items are done as examples. If your answer needs a special explanation, then give it.

6:78 Suziko lost the election. I conclude this because I know that if she lost the election, she is depressed. And clearly she is depressed.
*Final conclusion: Suziko lost the election. AC; DI*

6:79 If John is at work today, then Juanita is happy. If Juanita is happy, then she is smiling. I just saw Juanita and noticed that she was not smiling. Hence, John is not at work today.
*Final conclusion: John is not at work today. DC, DC; DV*

6:80 Karl did not lose the election. I conclude this because I know that if he lost the election, he would be depressed. And he obviously is not depressed.

6:81 If Mary went out last night, then Pedro is angry today. I have just seen Pedro and he is not angry today. Therefore, Mary did not go out last night.

6:82 Terry is in trouble, if she lied about her age. Therefore, if Terry is in trouble, then she lied about her age.

6:83 Terry lied about her age, if she managed to get into the Blue Room. But Terry did not manage to get into the Blue Room. We saw her at Shack's Fish & Chips. From all this, it follows that she did not lie about her age.

6:84 If John is in school, then Mary is happy. Hence, if Mary is unhappy, then John is not in school.

6:85 There is not a shortage of concrete. I conclude this from the fact that if the supervisor forgot us, there would be a shortage of concrete. But the supervisor never forgets us and she has not done so this time.

6:86 This blood on the porch is type A. If the blood is Al's blood, then it is type A, according to the blood analyst. Hence, the blood on the porch is Al's.

6:87 Tom Jeffers, if he was seen in the hospital waiting room at 10 P.M. and at midnight, did not do it. Someone claimed to see him, but the identification was a mistake. Because he really was not seen in the hospital waiting room at 10 P.M. and at midnight, he did it.

6:88 If it has not been proven beyond a reasonable doubt that she knew that at least there was a strong probability that she would do him serious harm, then she is not guilty. However, it has been proven beyond a reasonable doubt that she knew that there was a strong probability that she would do him serious harm. Therefore, she is guilty.
(Suggestion: Use *PBRD* to stand for *proven beyond a reasonable doubt*.)

6:89 Arlene did not admit that she did it, if she did not do it. But she did admit that she did it. Clearly then, she did it.

6:90 Joanna is not a liberal, if she did not support the prime minister. Therefore, if she supported the prime minister, she is a liberal.

6:91 If the hogs are not behaving strangely, then they did not eat thistles recently. But they are behaving strangely. From all this, I conclude that they ate thistles recently.

6:92 If Michael has a conflict of interest, then his testimony is not to be trusted. If Michael's brother is a suspect, then Michael has a conflict of interest. Michael's brother is a suspect. Therefore, Michael's testimony is not to be trusted.

6:93 If Shakespeare had intended Polonius to be a comic figure, then he would not have made Polonius the father of two tragic characters. But Polonius was made the father of two tragic characters, Laertes and Ophelia. Hence, Polonius was not intended by Shakespeare to be a comic figure.

6:94 No photosynthesis can be occurring in this plant. That this is so can be seen from the fact that it is not getting any light whatsoever. Furthermore, photosynthesis cannot occur in this plant, if there is no light reaching it.

6:95 If the Board of Education suspends young Brown from school, then it will be punishing him for refusing on religious grounds to salute the flag. And if it does that, it will be acting unconstitutionally. Because the board, we can be sure, will not act unconstitutionally, we can be sure that the board will not suspend young Brown.

6:96 If Arlene did not intentionally perform the act that caused Al's death, then she is not guilty. But the prosecutor has proven beyond a reasonable doubt that Arlene did intentionally perform the act that caused Al's death. Therefore, she is guilty.

6:97 Martin is wearing a red hat, if he thinks that hunters might be around. We just saw him and noticed that he is wearing a red hat. Therefore, he thinks that hunters might be around.

6:98 It has not been proven beyond a reasonable doubt that she believed that she was not safe. Therefore, it has been proven beyond a reasonable doubt that she believed that she was safe.

6:99 If she believed that he wanted to hurt her, then it has not been proven beyond a reasonable doubt that she was not justified in using the force that she used. It is clear that she really did believe that he wanted to hurt her. Therefore, it has been proven beyond a reasonable doubt that she was justified in using the force that she used.

### More Short Answer
For the following sets of reasons, if a conclusion that is different from the reasons follows necessarily, write it in. Otherwise write *Nothing*, by which you should mean that the conclusion that is probably intended does not follow necessarily. In any case, label the form of the probably intended argument. The first is done as an example.

6:100 If Anita stands to make a profit from your believing what she says, then you should be careful about believing what she says. It is clear that you should be careful about believing what she says. Therefore?
*Nothing; AC*

6:101 The spectator was lying, if the motorist told the truth about the accident. The spectator was certainly lying. Therefore?
6:102 If Amandita believes John, then she is a fool. However, Amandita is no fool. Therefore?
6:103 If our leader tells you to commit suicide, then he is not worthy of being our leader. By ordering you to drink the poison, our leader has in effect told you to commit suicide. Therefore?
6:104 Mr. Davis, if he was suspected to have a friendship with someone involved in the trial, was excused from the jury by the judge. Mr. Davis was excused from the jury by the judge. Therefore?

6:105 If Frankie did not step out of bounds, then the basket counts. But see, the referee is declaring that the basket does not count. Therefore?
6:106 John, if Jane said "No," went to the movies alone. John did not go to the movies alone. Therefore?
6:107 If the state has not proven beyond a reasonable doubt that she was not justified in using the force that she used, then she is not guilty. However, the state has proven beyond reasonable doubt that she was not justified in using the force that she used. Therefore?
6:108 If Arlene did not believe that circumstances existed that would justify the killing of Al, then she is not guilty of voluntary manslaughter. However, Arlene did believe that such circumstances existed. She was very jealous and believed that he was disloyal to her. Therefore?

## Saving Time with Letters

In propositional logic, we can save time in organizing arguments by using letters to represent each significant proposition in an argument. An arrow is used to show the *if-then* relationship. This system helps us show not only the overall picture, but also the way the parts are put together in complex propositions. This in turn helps us to decide whether the argument is deductively valid.

For propositional assignments, it is fairly traditional to use small letters, starting with *p*, then *q*, then *r*, etc. We assign a different letter to each basic proposition, generally using *p* to represent the antecedent. For our standard Ben example:
Let *p* = *Ben is a cat*.
Let *q* = *Ben is an animal*.

If you prefer, you can instead assign letters that have some connection with the proposition. For example, the assignment could be as follows:
Let *bc* = *Ben is a cat* (*b* for Ben; *c* for cat).
Let *ba* = *Ben is an animal*.

With these assignments, our standard *affirming-the-antecedent* example looks like this:

#### Example 6:18

|  |  |  |  |
| --- | --- | --- | --- |
| a. If Ben is a cat, Ben is an animal. |  | $p \rightarrow q$ | $md \rightarrow ma$ |
| b. Ben is a cat. | OR | $\underline{p}$ | $\underline{bc}$ |
| c. Therefore, Ben is an animal. |  | Therefore, $q$ | Therefore, $ba$ |

The fact that *p* (or *bc*) is to the left of the arrow shows it to be the antecedent in *a*. It is this same thing that is affirmed in *b*, so the argument is a case of affirming the antecedent. You knew this all along, but the example is helpful in showing how to use letters and arrows.

Henceforth, I shall use the traditional letter assignments (*p*, *q*, *r*, etc.). You should use whatever letter system you prefer.

The negation of the proposition *p* is represented by *not p*, meaning *It is not the case that* p. Here is a symbolization of an argument of the form, denying the consequent, using the same assignment of *p* and *q* as was used previously:

#### Example 6:19
| | |
| --- | --- |
| a. If Ben is a cat, then Ben is an animal. | a. $p \rightarrow q$ |
| b. Ben is not an animal. | b. $\underline{not\ q}$ |
| c. Therefore, Ben is not a cat. | c. Therefore, not $p$ |

Sometimes it is convenient to assign a letter to a proposition containing a negation, instead of showing the negation of a proposition. Consider the argument in Example 6:20:

#### Example 6:20
a. Tom Jeffers did not do it, if he was seen in the hospital waiting room between 10 P.M. and midnight.
b. He was seen in the hospital waiting room between 10 P.M. and midnight.
c. Therefore, he did not do it.

Let $p$ = *He was seen in the hospital waiting room between 10 P.M. and midnight*.
Let $q$ = *Tom Jeffers did not do it*. (The negation, *not*, is here treated as part of $q$.)

The argument can be represented as in Example 6:21:

#### Example 6:21
a. $p \rightarrow q$
b. $\underline{p}$
c. Therefore, $q$

Here is an assignment of letters that changes the assignment for *q*, although it makes the same assignment for *p*.

Let $p$ = *He was seen in the hospital waiting room between 10 P.M. and midnight*.
Let $q$ = *Tom Jeffers did it*. (The negation here is not treated as part of $q$.)

In this new assignment for $q$, the *not* has been omitted from the proposition to which $q$ is assigned. So, we must take care of this fact in representing the argument:

#### Example 6:22
a. $p \rightarrow$ not $q$
b. $\underline{p}$
c. Therefore, not $q$

Examples 6:21 and 6:22 are two different ways of representing the same argument. I find the first way more convenient; you might prefer the second. Either way is all right, as long as you stay with your original assignment throughout your analysis of the argument. Be consistent.

### Summary
In evaluating complicated deductive arguments, it is often helpful to assign individual letters to propositions and to represent the argument in terms of these letters. Use arrows to represent *if-then* relationships, and the word *not* to represent negation. In so doing, make sure that the same letter represents the same proposition throughout the argument.

## Check-Up 6D
**True or False?**
If a statement is false, change a crucial word or words to make it true.

6:109 Small letters are generally used to represent propositions.
6:110 The *q if p* relationship is represented by *p → q*.
6:111 In the symbolization, *q → r*, the antecedent is *q*.
6:112 In the symbolization, *r → p*, the consequent is *p*.
6:113 The following symbolized lines of reasoning are deductively valid:
  1. a. *p → q*
     b. *not q*
     c. Therefore, not *p*
  2. a. *p → not q*
     b. *p*
     c. Therefore, not *q*

6:114 The following symbolized lines of reasoning are deductively invalid:
  1. a. *p → not q*
     b. *not q*
     c. Therefore, *p*
  2. a. *p → not q*
     b. *q*
     c. Therefore, not *p*

6:115 The form of example #1 in 6:113 is *denying the consequent*.
6:116 The form of example #2 in 6:113 is *affirming the antecedent*.
6:117 The form of example #1 in 6:114 is *denying the consequent*.
6:118 The form of example #2 in 6:114 is *affirming the consequent*.

### Short Answer
For the next items, assign letters to the propositions, and represent the total statement in symbols. The first is done as an example.

6:119 If John is in school, then Mary is happy.
Let *p* = *John is in school*.
Let *q* = *Mary is happy*.
*p* → *q*

6:120 If Karl lost the election, then he was depressed.
6:121 Estelle is happy if Marguerite is here.
6:122 Karl lost the election if he was depressed.
6:123 The supervisor forgot about us if there is a shortage of concrete.
6:124 The cattle, if junipers are poisonous, are in danger.

For the next set of items, state the final conclusion, assign letters, represent the argument symbolically, label the type of logical move, and judge the validity. Show your judgment as before, using *AA, DA, AC, DC, CONTR, CONV, EDN, or NDN*, and *DV* or *DI*. You have seen these items before. They are presented here again for practice in using symbols. By doing the same items both ways, you can see whether symbols make things like this easier for you. The first is done as an example.

6:125 If John is at work today, then Juanita is happy. I just saw Juanita and noticed that she is happy. Therefore, John is at work today.

Final conclusion: John is at work today.
Let *p* = *John is at work today*.
Let *q* = *Juanita is happy*.
*p* → *q*
*q*
Therefore, *p*  AC, DI

6:126 If Pedro went out last night, then Mary is angry today. I have just seen Mary and she is not angry today. Therefore, Pedro did not go out last night.
6:127 Suziko lost the election. I conclude this because I know that if she lost the election, she is depressed. And clearly she is depressed.
6:128 Terry, if she lied about her age, is in trouble. But she is not in trouble, so she did not lie about her age.
6:129 Terry lied about her age, if she managed to get into the Blue Room. But Terry did not manage to get into the Blue Room. We saw her at Shack's Fish & Chips. From all this, it follows that she did not lie about her age.
6:130 This blood on the porch is type A. If the blood is Al's blood, then it is type A, according to the blood analyst. Hence, the blood on the porch is Al's.
6:131 Joanna is not a liberal, if she did not support the prime minister. Therefore, if she supported the prime minister, she is a liberal.

6:132 If it has not been proven beyond a reasonable doubt that she knew that at least there was a strong probability that she would do him serious harm, she is not guilty. However, it has been proven beyond a reasonable doubt that she knew that at least there was a strong probability that she would do him serious harm. Therefore, she is guilty.

6:133 If the Board of Education suspends young Brown from school, then it will be punishing him for refusing on religious grounds to salute the flag. And if it does that, it will be acting unconstitutionally. Because the board, we can be sure, will not act unconstitutionally, we can be sure that the board will not suspend young Brown.

6:134 If Michael has a conflict of interest, then his testimony is not to be trusted. If Michael's brother is a suspect, then Michael has a conflict of interest. Michael's brother is a suspect. Therefore, Michael's testimony is not to be trusted.

## Conjunction, Alternation, and Embedded Complex Propositions

In the following argument (which you saw at the beginning of this chapter), two propositions are conjoined (connected by the word *and*). The two are then treated as one unit and become the antecedent for the overall implication. Can you assign letters and judge the deductive validity? The basic propositions are italicized:

**Example 6:23**
If *parking is prohibited on this street* and *Sybil parked there last night*, then *Sybil is in trouble*. However, I know that *Sybil is not in trouble*, and that *parking is prohibited on this street*. Therefore, *she did not park there last night*.

Try it before I discuss it in the next section.

### Conjunction and Embedded Complex Propositions

The propositions in Example 6:23 can be assigned letters as follows:
Let *p* = *Parking is prohibited on this street*.
Let *q* = *Sybil parked there last night*.
Let *r* = *Sybil is in trouble*.

The first two propositions are joined together by the word *and*, as in *p and q*. The way to show that they jointly form the antecedent is to put parentheses around them before adding the arrow to show implication, as in Example 6:24:

**Example 6:24**
(*p* and *q*) → *r*

Thus, *p* and *q* are conjoined and the conjunction is *embedded* in the whole implication.

The first step in the argument is the denial of the consequent, *r*, resulting in the denial of the conjunction:

#### Example 6:25
```
(p and q) → r
not r
Therefore, not (p and q)
```

It is important to retain the parentheses in the conclusion of Example 6:25 since it is the whole conjoined unit that is being denied, not any individual part. This conclusion can be read, "Not both *p* and *q*." The conclusion does not tell us which of the parts is denied. It only tells us that at least one is to be denied (or perhaps both). The next step in the argument clarifies this because the original argument asserts *p*. The next step is reasoning from a denied conjunction, one part of which is affirmed:

#### Example 6:26
```
not (p and q) (This is the conclusion of Example 6:25. We use it in this next step.)
p
Therefore, not q
```

If one part of a denied conjunction is affirmed, the other must be denied. They cannot both be accepted, so the argument is deductively valid. The conclusion of Example 6:23, "She did not park there last night," follows necessarily from the reasons given.

This type of argument will appear again in Chapters 8 and 9 in connection with the refutation of hypotheses. It is a combination of *denial of the consequent* and *affirmation of one part of a negated conjunction*. This last label is long and awkward, but at least it describes what happens. There is no good label for it without inventing another technical term.[^4]

When a conjunction of propositions appears by itself, and is affirmed, then it is implied that each conjunct can be affirmed separately. For example, if someone said, "Parking is prohibited on this street and Sybil parked there yesterday," it would deductively follow from the conjunction that parking is prohibited on this street. But if the conjunction is denied, and there is no other information, then the denial of each or either does not follow deductively. All that we know then is that at least one is to be denied, but we do not yet know which one.

[^4]: This is a controversial point, again beyond the scope of this book. See the Lewis, Strawson, and Grice references mentioned at the beginning of Chapter 5 if you want to pursue it.

### Alternation
An alternation consists of two propositions (alternants) connected by the word *or*, as in *Myrna is going back to California, or she is foolish*. The denial of either alternant then implies the assertion of the other. Suppose that Myrna is not going back to California. It follows that she is foolish. Suppose that she is not foolish. It follows that she is going back to California. Example 6:27 illustrates the first of these two deductively valid arguments.

#### Example 6:27
Let *p* = *Myrna is going back to California*.
Let *q* = *She is foolish*.
| | |
| --- | --- |
| a. Myrna is going back to California, or she is foolish. | *p* or *q* |
| b. Myrna is not going back to California. | not *p* |
| c. Therefore, she is foolish. | Therefore, *q* |

Denial of an alternant; DV


Example 6:28 illustrates the denial of the other alternant:

#### Example 6:28
| | |
| --- | --- |
| a. Myrna is going back to California, or she is foolish. | *p* or *q* |
| b. Myrna is not foolish. | not *q* |
| c. Therefore, Myrna is going back to California. | Therefore, *p* |

Denial of an alternant: DV

On the other hand, the affirmation of either of these alternants does not imply the denial of the other. For example, suppose that Myrna *is* foolish. That does not imply that she is not going back to California. Her going is not precluded by the alternation and her being foolish. She might go for some foolish reason. Similarly, suppose that she *is* going back to California. That, together with the alternation, does not imply that she is not foolish. Again, she might be going back for some foolish reason. Example 6:29 presents this latter case.

#### Example 6:29
| | |
| --- | --- |
| a. Myrna is going back to California, or she is foolish. | *p* or *q* |
| b. Myrna is going back to California. | *p* |
| c. Therefore, she is not foolish. | Therefore, not *q* |

Affirmation of weak alternant; DI

&#43; However, in a strong sense of the word *or*, the affirmation of either alternant does imply the denial of the other, as in *Either Marguerite is at the movies or she is with Estelle*. Example 6:30 illustrates the use of the strong *or*.

#### Example 6:30
Let *p* = *Marguerite is at the movies*.
Let *q* = *She is with Estelle*.
| | |
| --- | --- |
| a. *Either* Marguerite is at the movies *or* she is with Estelle.  | *p or q* |
| b. Marguerite is at the movies.  | *p* |
| c. Therefore, she is not with Estelle. Therefore, not  | *q* |
Affirmation of strong alternant;

&#43; You must decide from the situation which sense of *or* is in use, the weak sense (as in Examples 6:27, 6:28, and 6:29), or the strong sense (as in Example 6:30). But remember, there is no free ride. If the strong sense is in use, the alternation reason (*a*) is harder to establish, so the total argument might be in trouble if the strong sense is in use. If in doubt, I suggest the weak interpretation.

### Summary
When two propositions are *conjoined* by the word *and*, they form a unit. If the whole unit is asserted, that implies that each *conjunct* can be asserted separately. If the unit is denied (or negated), then at least one conjunct must be denied. Without further information, it is not clear which one is the one to be denied. Furthermore, the unit can itself be a proposition in an argument (as can any complex proposition). This is shown by the use of parentheses around the unit when it is represented symbolically.

When two propositions are connected by the word *or*, they are *alternants*. The denial of one alternant implies the assertion of the other, if the total alternation is asserted.

&#43; However, unless the alternation is a *strong* alternation, the assertion of one alternant does not imply the denial of the other. You must determine from the situation whether the *or* is strong or weak. If in doubt, I suggest that you choose the weak interpretation.

## Check-Up 6E
**True or False?**
If the statement is false, change a crucial word or words to make it true.
6:135 The affirmation of one conjunct implies the denial of the other.
6:136 The denial of one weak alternant implies the affirmation of the other.
6:137 Affirming a conjunct in a negated conjunction is a deductively valid move.
6:138 Denying a conjunct in a negated conjunction is a deductively valid move.
6:139 There is little practical difference between these two complex propositions: (1) *not (p and q)* and (2) *not p and q*.
&#43; 6:140 The affirmation of one strong alternant implies the denial of the other.
&#43; 6:141 The affirmation of one weak alternant implies nothing about the other.

### Short Answer
State the conclusion, assign letters, symbolize the argument, judge the deductive validity, and give your reason.

6:142 This piece of cloth is warm and it is 50 percent wool. If the dog is shivering from cold, then the cloth is not warm. Therefore, the dog is not shivering from cold.

6:143 If the label on this piece of cloth reads "50 percent wool," then it is 50 percent wool. This morning John, who knows about such things, said that the piece of cloth is warm, but it is only 25 percent wool. Therefore, the label certainly does not read "50 percent wool."

6:144 Thomas Jefferson did not make the mistake of which you are accusing him. If he had, then he would not have been an astute politician. But he was a scholar; he was a gentleman; and he was an astute politician.

6:145 Either there will be rain within the week, or the crops will be ruined. We can be sure that it will not rain within the week. Hence, we can be sure that the crops will be ruined.

&#43; 6:146 The two colors that you select will match or the room will be ugly. If I help you select the colors, then they will match. I am going to help you select the colors. Therefore, the room will not be ugly.

6:147 Abraham Lincoln must have thought that his Gettysburg Address was a failure. The following reasons make this apparent: Either he thought that it was reverently received, or he thought that it was a failure. From his remarks made immediately afterward, we can be sure that he did not think that it was reverently received.

6:148 If Dick took a driver training course and passed it with a grade of B or higher, then he is entitled to a lower rate on automobile insurance. Dick did take a driver training course. Therefore, he is entitled to a lower rate on automobile insurance.

6:149 I believe that Tom Jeffers did not stab Al. Here's why: Either Tom was in the hospital when the stabbing took place five miles away or, during the ten minutes when he was not under observation, he managed to travel to the site, spend some time, and return. If he did all that, then he is superman—and we all know he is not anything like superman. Not Tom Jeffers. If he was in the hospital when the stabbing took place, then he did not stab Al. I rest my case.

6:150 If Pedro has lived in his election district for over thirty days, and is over eighteen, he is entitled to vote. Pedro has lived in his election district for over a year, and he turned nineteen last month. Therefore, he is entitled to vote.

6:151 Hamlet must not have been in doubt of the guilt of his uncle. Consider: He certainly was not both in doubt of the guilt of his uncle and convinced that he had actually spoken to his father's ghost. He was convinced that he had actually spoken to his father's ghost. Hence, in his mind there was no doubt of the guilt of his uncle.

6:152 You have seen rainbows when it was raining, and you have seen rainbows when it is sunny. But one thing is certain: It is not the case both that there is a rainbow now and that the sky is completely overcast now. You will note that there is no rainbow now. From this, it follows that the sky is completely overcast now. There is no way around it.

6:153 It is not true both that Sheila is in love with Jim and at the same time in love with John. Nobody can be in love with two different people at the same time. From all we can see, it is clear that Sheila is in love with Jim. Therefore, Sheila is not in love with John.

6:154 I do not agree that it is not possible to be in love with two people at the same time. But be that as it may, I still think that we can conclude that Sheila is not in love with John. Here's why: If Sheila is in love with John, then she will have secured John's signature in her yearbook. Now she did not both secure John's signature in her yearbook and go to the dance with Jim. If she did not go to the dance with Jim, then she is at home right now. I just checked, and she is not at home, so you can see why I think that she is not in love with John. It follows.

6:155 Arlene is not both guilty of murder and innocent of voluntary manslaughter. If she might have been justified in using the amount of force she used, then she is innocent of voluntary manslaughter. Therefore, she is not guilty of murder because she might have been justified in using the amount of force she used.

## Suggested Answers for Chapter 6

### Check-Up 6A
6:1 T &nbsp;&nbsp; 6:2 F &nbsp;&nbsp; 6:3 T &nbsp;&nbsp; 6:4 F &nbsp;&nbsp; 6:5 T &nbsp;&nbsp; 6:6 T  
6:7 F &nbsp;&nbsp; 6:8 F  

6:2 Omit clause starting with *but*.  
6:4 Replace *is the same* with *in one is the consequent in the other*.  
6:7 Change *first* to *after the if*.  
6:8 Move the *if* to the beginning of the first clause in *a*.  
6:9–6:10 These were done as examples.  
6:11–6:28 The antecedent is *a* and the consequent is *b*:  
6:11 a. junipers . . . poisonous  
b. the cattle . . . in danger  
6:12 a. junipers . . . poisonous  
b. The cattle . . . in danger  
6:13 a. the supervisor . . . us  
b. there . . . concrete  
6:14 a. Terry . . . Room  
b. she . . . age  
6:15 a. Terry . . . age  
b. she . . . Room  
6:16 a. Joanna . . . liberal  
b. she . . . minister

6:17 a. she . . . minister  
b. Joanna . . . liberal  

6:18 a. Arlene admitted . . . it  
b. she did it  

*Note: Henceforth in this set, odd-numbered answers will be omitted.*

6:20 a. she admitted . . . it  
b. Arlene did it  

6:22 a. she . . . death  
b. she . . . him  

6:24 a. it . . . A  
b. The blood . . . blood  

6:26 a. Tom . . . midnight  
b. he did not do it  

### Check-Up 6B
6:27 T &nbsp;&nbsp; 6:28 T &nbsp;&nbsp; 6:29 T &nbsp;&nbsp; 6:30 F &nbsp;&nbsp; 6:31 T  
6:30 Change *valid* to *invalid*.  
6:32 Done as an example.  
6:33 DC, DV &nbsp;&nbsp; 6:34 AC, DI &nbsp;&nbsp; 6:35 DC, DV &nbsp;&nbsp; 6:36 AC, DI  
6:37 DA, DI &nbsp;&nbsp; 6:38 AC, DI &nbsp;&nbsp; 6:39 Deliberately omitted.  
6:40 DC, DV &nbsp;&nbsp; 6:41 Deliberately omitted.  

### Check-Up 6C
6:42 T &nbsp;&nbsp; 6:43 F &nbsp;&nbsp; 6:44 T &nbsp;&nbsp; 6:45 T &nbsp;&nbsp; 6:46 T &nbsp;&nbsp; 6:47 T  
6:48 F &nbsp;&nbsp; 6:49 T &nbsp;&nbsp; 6:50 T &nbsp;&nbsp; 6:51 F &nbsp;&nbsp; 6:52 T  
6:43 Change *the converse of* to *the same as*.  
6:48 Two negatives usually make a positive.  
6:51 One way: Exchange the antecedent and the consequent in the second reason.  
6:53 Done as an example.  
6:54 [Blank] . . . if  
6:55 If . . . then  
6:56 If . . . then  
6:57 Deliberately omitted.  
6:58 Done as an example.  
6:59 Motorcycles are permitted.  
6:60 The diamond is in the queen's crown.  
6:61 Not eliminable.  
6:62 If Arlene did it, then she admitted that she did it.  
6:63 Deliberately omitted.  
6:64 Not eliminable.  
6:65 Deliberately omitted.  
6:66 Not eliminable because one negation is in an antecedent and the other in a consequent.  
6:67 If Arlene did not do it, then she did not admit doing it.

6:68 If our cattle are not ill, then junipers are not poisonous.
6:69 If the blood is not type A, then it is not Al's blood.
6:70 If the vehicle is not prohibited, then it does not have a motor.
6:71 If Sara Lee was admitted to the Panama Club, she lied about her age.
6:72 If we do not have enough concrete, the supervisor forgot about us.
6:73 If Martin does not think that hunters might be around, then he is not wearing a red hat.
6:74 If Shiboen did not buy it, then the gift is not inexpensive.
6:75 Deliberately omitted.
6:76 If the battery is not in bad condition, then you did not leave the lights on all night.
6:77 Deliberately omitted.
6:78–6:79 These were done as examples.
6:80 Karl did not lose the election. DC; DV
6:81 Mary did not go out last night. DC; DV
6:82 If Terry is in trouble, then she lied about her age. CONV; DI
6:83 She did not lie about her age. DA; DI
6:84 If Mary . . . school. CONTR; DV
6:85 There is not a shortage of concrete. DA; DI
6:86 The blood on the porch is Al's. AC; DI
6:87 He did it. DA; DI
6:88 She is guilty. DA; DI
6:89 She did it. DC; DV
6:90 If she supported the prime minister, she is a liberal. CONV of CONTR; DI.

*Note: This last item is more complicated than the previous ones in that the conclusion is neither simple conversion nor contraposition. Rather, it can be viewed as the conversion of the contrapositive (or the contraposition of the converse). The contrapositive of the original assertion is *If she is a liberal, then she supported the prime minister*. This would follow necessarily, but the proposed conclusion is the converse of this.*

Henceforth in this set and the next, odd-numbered answers are omitted.
6:92 Michael's testimony is not to be trusted. AA, AA; DV
6:94 No photosynthesis can be occurring in this plant. AA; DV
6:96 She is guilty. DA; DI
6:98 It has been PBRD that she believed she was safe. NDN DI
6:100 Done as an example.
6:102 Amandita does not believe John. DC
6:104 Nothing. AC
6:106 Jane did not say "No." DC
6:108 Nothing. DA

### Check-Up 6D
6:109 T &nbsp;&nbsp; 6:110 T &nbsp;&nbsp; 6:111 T &nbsp;&nbsp; 6:112 T &nbsp;&nbsp; 6:113 T  
6:114 F &nbsp;&nbsp; 6:115 T &nbsp;&nbsp; 6:116 T &nbsp;&nbsp; 6:117 F &nbsp;&nbsp; 6:118 F  
6:114 #1 is deductively invalid, but not #2.

6:117 Replace *denying* with *affirming*.
6:118 Replace *affirming* with *denying*.
6:119 Done as an example.
6:120 
Let *p* = *Karl lost the election*.  
Let *q* = *he was depressed*.  
*p* → *q*

6:121 
Let *p* = *Marguerite is here*.  
Let *q* = *Estelle is happy*.  
*p* → *q*

6:122 
Let *p* = *he was depressed*.  
Let *q* = *Karl lost the election*.  
*p* → *q*

6:123 Deliberately omitted.
6:124 
Let *p* = *junipers are poisonous*.  
Let *q* = *The cattle are in danger*.  
*p* → *q*

6:125 Done as an example.
6:126 Final conclusion: Pedro did not go out last night.  
Let *p* = *Pedro went out last night*.  
Let *q* = *Mary is angry today*.  
*p* → *q*  
not *q*  

Therefore, not *p* &nbsp;&nbsp; DC; DV

6:127 Final conclusion: Suziko lost the election.  
Let *p* = *Suziko lost the election*.  
Let *q* = *she is depressed*.  
*p* → *q*  
*q*  

Therefore, *p* &nbsp;&nbsp; AC; DI

6:128 Final conclusion: She did not lie about her age.  
Let *p* = *she lied about her age*.  
Let *q* = *Terry is in trouble*.  
*p* → *q*  
not *q*  

Therefore, not *p* &nbsp;&nbsp; DC; DV

6:129 Final conclusion: She did not lie about her age.  
Let *p* = *she managed to get into the Blue Room*.  
Let *q* = *Terry lied about her age*.  
*p* → *q*  
Not *p*  


Therefore, not *q* &nbsp;&nbsp; DA; DI

6:130 Final conclusion: The blood on the porch is Al's.  
Let *p* = *the blood is Al's*.  
Let *q* = *the blood is type A*.  
*p* → *q*  
*q*  


Therefore, *p* &nbsp;&nbsp; AC; DI

Henceforth in this set, odd-numbered answers are omitted.

6:132 Final conclusion: She is guilty.  
Let *p* = *it has not been PBRD . . . harm*.  
Let *q* = *she is not guilty*.  
*p* → *q*  
not *p*  


Therefore, not *q* &nbsp;&nbsp; DA; DI

6:134 Final conclusion: Michael's testimony is not to be trusted.  
Let *p* = *Michael has a conflict of interest*.  
Let *q* = *his testimony is not to be trusted*.  
Let *r* = *Michael's brother is a suspect*.  
*r* → *p*  
*p* → *q*  
*r*  


Therefore, *q* &nbsp;&nbsp; AA, AA; DV

### Check-Up 6E
6:135 F &nbsp;&nbsp; 6:136 T &nbsp;&nbsp; 6:137 T &nbsp;&nbsp; 6:138 F &nbsp;&nbsp; 6:139 F  
6:140 T &nbsp;&nbsp; 6:141 T  
6:135 Replace *the denial of* with *nothing about*.  
6:138 Change *valid* to *invalid*.  
6:139 Change *little practical* to *a great*.

6:142 Conclusion: The dog is not shivering from the cold.  
Let *p* = *this piece of cloth is warm*.  
Let *q* = *it is 50 percent wool*.  
Let *r* = *the dog is shivering from cold*.  
*p* and *q*  
*r* → not *p*  


Therefore, not *r* &nbsp;&nbsp; DC; DV

6:143 Conclusion: The label does not read "50 percent wool."  
Let *p* = *the label reads "50 percent wool."*  
Let *q* = *it is 50 percent wool*.  
Let *r* = *the piece of cloth is warm*.  
*p* → *q*  
*r* and not *q*  


Therefore, not *p* &nbsp;&nbsp; DC; DV

6:144 Conclusion: Thomas Jefferson did not make . . . him.  
Let *p* = *Thomas Jefferson made . . . him*.  
Let *r* = *he was an astute politician*.  
Let *s* = *he was a scholar*.  
Let *t* = *he was a gentleman*.  
*p* → not *r*  
*s* and *t* and *r*  


Therefore, not *p* &nbsp;&nbsp; DC; DV

Henceforth in this set, odd-numbered answers are omitted.

&#43; 6:146 Conclusion: The room will not be ugly.  
Let *p* = *the two colors you select will match*.  
Let *q* = *the room will be ugly*.  
Let *r* = *I help you select the colors*.

Argument in steps:
Step 1:
*r* → *p*
*r*


So, *p* (AA; DV)

Step 2
*p* or *q*
*p*


Therefore, not *q* (affirmation of weak alternant; DI)

Total argument:
*p* or *q*
*r* → *p*
*r*


Therefore, not *q*
AA, Affirmation of weak alternant (AWA); DI

*Note:* If you interpreted the *or* as strong, the argument would have been deductively valid, but then it would have been more difficult to establish the alternation *p or q*.

6:148 Conclusion: He is entitled . . . insurance.
Let *p* = *Dick took a driver training course*.
Let *q* = *he passed it with a grade of B or higher*.
Let *r* = *he is entitled . . . insurance*.
(*p* and *q*) → *r*
*p*


Therefore, *r*
Only one conjunct in the antecedent was affirmed; DI

6:150 Conclusion: He is entitled to vote.  
Let *p* = *Pedro has lived in his election district for over thirty days*.  
Let *q* = *he is over eighteen*.  
Let *r* = *he is entitled to vote*.  
(*p* and *q*) → *r*  
*p* and *q*  


Therefore, *r* &nbsp;&nbsp; AA; DV

6:152 Conclusion: The sky is completely overcast now.  
Let *p* = *there is a rainbow now*.  
Let *q* = *the sky is completely overcast now*.  
not both *p* and *q*  
not *p*  


Therefore, *q* &nbsp;&nbsp; Affirming a negated conjunct (ANC); DI

6:154 Conclusion: Sheila is not in love with John.  
Let *p* = *Sheila is in love with John*.  
Let *q* = *she will have secured John's signature in her yearbook*.  
Let *r* = *she went to the dance with Jim*.  
Let *s* = *she is at home right now*.

Argument in steps:
Step 1:
not *r* → *s*  
not *s*  


So, *r* (DC; DV)

Step 2:
not (*q* and *r*)  
*r*  


So, not *q* (negation of conjunction; DV)

Step 3:
*p* → *q*  
not *q*  


Therefore, not *p* (DC; DV)

Total argument: All steps deductively valid; DV

6:156 Conclusion: She is not guilty of murder.  
Let *p* = *Arlene is guilty of murder*.  
Let *q* = *she is innocent of voluntary manslaughter*.  
Let *r* = *she might have been justified in using the amount of force she used*.  
not (*p* and *q*)  
*r* → *q*  
*r*  


Therefore, not *p* &nbsp;&nbsp; (DC, Affirm part of negated conj., DC; DV)