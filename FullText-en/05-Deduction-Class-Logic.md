# CHAPTER 5 Deduction: Class Logic

In Chapters 2, 3, and 4, our primary concerns were with analyzing arguments and appraising reasons. Now we turn to inference (*FRISCO's I*), the step from the reason(s) to the conclusion.

In Chapters 5 and 6, we shall look only at one kind of inference, basically the kind that has interested professional logicians: deductive inference. However, the approach to deductive inference in this book will be different from theirs because our purpose in critical thinking is practical and general, theirs theoretical and abstract, making theirs heavily symbolic. Although their symbolic approach is very valuable for certain purposes of philosophers, mathematicians, computer scientists, and some others, it has drawbacks when used as a guide to the practical reasoning of people actually deciding what to believe or do. One drawback is the difficulty for most people of understanding its systems at even an elementary level. A second is that most of these systems are occasionally misleading as guidelines to reasoning.[^1]

Because the approach to deductive logic you will see here is simple, practical, more intuitive, and usable from the outset of your study, there is much value in it. But if you are looking for an elegant, abstract, symbolic system, you will not find it here. For that, you should go to a standard deductive-logic textbook.

In this chapter, you will be introduced to the meaning of the central question in deductive inference: Does a conclusion follow necessarily from one or more other propositions? You will also learn a few specific techniques for handling some standard kinds of deductive arguments. These will give you a good start, but realize that there are many other techniques and possible refinements.

For some people, the material in Chapters 5 and 6 is easy. For others, it is difficult. If it is difficult for you, find someone for whom it is easy, and ask for help. If it is easy for you, help someone. By so doing, both parties will actually learn much more than they would otherwise.

[^1]: This is a controversial topic, beyond the scope of this book, but those who are interested might start with a look at C. I. Lewis' "Implication and the Algebra of Logic," *Mind*, October 1912, pp. 522–531, and P. F. Strawson's *Introduction to Logical Theory* (London: Methuen & Co., 1952), where some misleading features are elaborated. H. P. Grice, in his "Logic and Conversation," in *The Philosophy of Language* (2nd edition), edited by A. P. Martinich (Oxford: Oxford University Press, 1990), offers a defense.


## Deductive Validity and Invalidity

Let us start with the basic concept in deductive inference: *deductive validity*. To say that an argument is *deductively valid* is to say that its conclusion follows necessarily from its reasons. That is to say, if you accept the reasons in a deductively valid argument, you are thereby automatically committed to accepting the conclusion. In a deductively valid argument, it would be contradictory to reject the conclusions if you accept the reasons. Consider this argument:

**Example 5:1**

Look, you do realize that if Ben is a cat, then Ben is an animal. And Ben definitely is a cat. So, it follows that Ben is an animal.

As usual, the first thing is to identify the conclusion (the *F* in *FRISCO*), which is "Ben is an animal." Then we look for the reasons (*FRISCO's R*), which are *a* and *b* in Example 5:2. Reducing the argument to its minimum features, it becomes:

**Example 5:2**

a. If Ben is a cat, then Ben is an animal.
b. Ben is a cat.
c. Therefore, Ben is an animal.

In this argument, the conclusion follows necessarily from the combination of reasons, *a* and *b*. That is, if you accept *a* and *b*, you are automatically committed to accepting *c*. There is no way to avoid it. The argument is deductively valid. Make sure that you see this utter unavoidability of the conclusion, given the reasons. It is the essential feature of deductive validity.

This concept of deduction is different from that of Sherlock Holmes. Generally, his "deduced" conclusions were based on inductive inference, a type of inference we shall consider soon, starting in Chapter 8. His conclusions generally were supported by very strong evidence, but were not absolutely unavoidable. For example, in *The Sign of the Four*, when he concluded that a man with a wooden leg had been in the victim's room, there were other possible explanations for the fact that there were marks on the floor like the marks that would have been made by a wooden leg. The marks on the floor might have been made by someone else in order to implicate the man with the wooden leg. Thus, we are not inescapably committed to Holmes' conclusion on the basis of his evidence. At best, most of his "deduced" conclusions followed "beyond a reasonable doubt," the standard used in criminal trials in contemporary courts.


Deductive validity is a much more stringent standard. Given the reasons in a deductively valid argument, there is absolutely no way to avoid the conclusion. But as you will come to see, this standard is an ideal about which we often need to make compromises in practical situations. More about these compromises later. But before you can consider the compromises, you must become familiar with the ideal.

Note that it is only the *relationship* between the reasons and the conclusion that we are talking about when we call an argument deductively valid. We are not talking about the conclusion—or the premises—in themselves. In particular, to call an argument deductively valid is *not* to say that the conclusion is true. Here is an example of a deductively valid argument with a *false* conclusion:

**Example 5:3**

a. Whales are large fish.
b. All large fish lay eggs.
c. Therefore, whales lay eggs.

In Example 5:3, if you accept *a* and *b*, you are automatically committed to accepting *c*, so the argument is deductively valid, even though the conclusion and the first premise are false.

There is a use for deductive arguments that lead to false conclusions. Such arguments are a way to show that one or more of the reasons are false: If a deductively valid argument has a false conclusion (as in Example 5:3), then we know that at least one of the reasons is false. Otherwise, the conclusion would have to be true because the argument is deductively valid. Suppose that there are only two reasons in a deductively valid argument with a false conclusion (as in Example 5:3). Then, if one of the reasons is true, the other must be false (because at least one has to be false). In Example 5:3, if we assume that *b* is true and *c* is false, then *a* must be false. Therefore, the deductive validity and the assumptions that *c* is false and *b* is true establish that *a* is false. That is, they establish that whales are not large fish. This is the standard kind of reasoning used in rejecting hypotheses.

You will read more about this later, but I discussed the example here to show that a deductively valid argument can have a false conclusion, and that there is a practical use for deductively valid arguments with false conclusions.

### Deductive Invalidity

A *deductively invalid* argument is one in which the conclusion does *not* necessarily follow from the reasons. Here is one:

**Example 5:4**

a. Fish are vertebrates.
b. Mammals are vertebrates.
c. Therefore, fish are mammals.


The fact that fish and mammals share a common characteristic, being vertebrates, does not require that fish be mammals. Here is another deductively invalid argument:

**Example 5:5**

a. Whales are vertebrates.
b. Mammals are vertebrates.
c. Therefore, whales are mammals.

In Example 5:5, even though the conclusion and the reasons are true, the conclusion does not follow necessarily from the reasons given. As in the fish argument, the fact that whales and mammals share a common characteristic does not require that whales be mammals. Whales are mammals, but this is not necessarily established by their sharing this common characteristic. If you do not see this, substitute *fish* for *whales* in Example 5:5. This substitution exhibits the deductive invalidity of the argument in Example 5:5. This sort of substitution is helpful in seeing deductive invalidity (or validity) when your beliefs about truth interfere with your judgments about deductive validity, or when the argument is too complicated or abstract for you to comprehend comfortably.

Examples 5:4 and 5:5 are helpful in several ways:

- They exhibit deductively invalid relationships.
- Example 5:5 shows that an argument can have a true conclusion even though it is deductively invalid.
- Together, the examples exhibit one technique for evaluating an argument: constructing a similar argument, the validity or invalidity of which is easy to see.

It is important to realize that deductive invalidity is often not a fatal flaw in an argument. Many good arguments are deductively invalid. An example was presented early in Chapter 2: the prosecutor's proof beyond a reasonable doubt that Arlene performed the act that caused Al's death.

### Summary

We have begun to look at one standard kind of inference: deductive inference. It is different from what Sherlock Holmes generally called "deduction," but is similar in basic spirit, though not in detail, to the deduction of symbolic logic. However, ours is the deduction of everyday reasoning. It is easier to learn this at the outset, and it avoids the occasionally misleading features of symbolic logic. It also lacks the elegance of symbolic logic, but it has practical uses, as you will see.

To say that an argument is *deductively valid* is to say that if the reasons are accepted, the conclusion must necessarily also be accepted. The truth of the reasons requires the truth of the conclusion if the argument is deductively valid. To say that an argument is not deductively valid is to say that the conclusion does not follow necessarily—although it might be true and well-established by the reasons, perhaps even proved beyond a reasonable doubt.

A deductively invalid argument can have a true conclusion, so showing an argument to be deductively invalid does not show the conclusion to be false. A deductively valid argument can have a false conclusion, if at least one of the reasons is false. It can also have a true conclusion together with false reasons. But showing an argument to be deductively valid, if the reasons are true, establishes that the conclusion is true. Furthermore, showing the conclusion of a deductively valid argument to be false establishes that at least one of the reasons is false.

In brief, any combination is possible but the combination of deductive validity, all true reasons, and a false conclusion. If you have any two of the three, you cannot have the third.

Although these points were illustrated with some examples, digesting them and feeling comfortable with them will probably require practice with and discussion of many more examples, including some that apply these basic ideas to your own specialty. Try to apply these ideas to examples in your own specialty, as well as to the examples provided here.

---

## Check-Up 5A

**True or False?**
If false, change it to make it true. Try to do so in a way that shows that you understand.

**5:1** A deductively valid argument is one in which the conclusion follows necessarily from the reasons.

**5:2** If an argument is deductively valid, acceptance of the reasons commits you to accepting the conclusion.

**5:3** Deductive validity is equivalent to proof beyond a reasonable doubt.

**5:4** If the conclusion of an argument is true, then the argument must be deductively valid.

**5:5** If the conclusion of an argument is false, then the argument must be deductively invalid.

**5:6** If the conclusion of a deductively valid argument is false, then one or more of the reasons is false.

**5:7** If the conclusion of an argument is false and the reasons are true, then the argument is deductively invalid.

### Short Answer

For each of the following arguments, decide whether you think it is deductively valid or deductively invalid. Use your basic understanding of deductive validity as I have explained it: If you accept the reasons, you are thereby committed to accepting the conclusion.

**5:8** 
a. Houses are buildings.
b. Buildings are structures.
c. Therefore, houses are structures.


**5:9** 
a. Motorcycles are vehicles.
b. Vehicles are mechanical contraptions.
c. Therefore, motorcycles are mechanical contraptions.

**5:10** 
a. Houses are structures.
b. Homes are structures.
c. Therefore, houses are homes.

**5:11** 
a. Birds have wings.
b. Ostriches are birds.
c. Therefore, ostriches have wings.

**5:12** 
a. No vehicles are permitted.
b. Motorcycles are vehicles.
c. Therefore, no motorcycles are permitted.

## Class Logic, Using a Circle System

Next, we shall consider one common type of deductive logic—class logic—the type that deals with relationships among classes and individuals. We shall use a circle system for dealing with class logic arguments.

### Inclusion

In this circle system, deductive arguments are represented by a set of circles (called Euler circles[^2]) and Xs, each circle representing a class. Xs represent individuals.

First, I shall represent the argument in Check-Up Item 5:8 with circles, so check back and read that argument. The purpose here is to show how the system works. You already know that the argument is deductively valid.

**Diagram 5:1**, using one circle, represents the class of buildings:

**Diagram 5:1**

[diagram]

To show that the class of houses is included in the class of buildings, a circle for houses is put inside the circle for buildings:

**Diagram 5:2**

[diagram]

[^2]: This system is largely based on one developed by Leonhard Euler, a Swiss mathematician. Professor William Rapaport has suggested useful changes.


**Diagram 5:2** is a picture of the relationship stated by reason *a* in Check-Up Item 5:8. That reason is, "Houses are buildings." The fact that the circle for houses is inside the circle for buildings pictures the relationship between houses and buildings that is asserted in reason *a*. It shows that houses are buildings; that is, the class of houses is included in the class of buildings. If that picturing is not clear to you, think about it for a while. This is an example of the basic relationship in this circle approach.

Although the word *all* is not in the original proposition, we draw diagrams as if it were, that is, as if the original were "All houses are buildings." It is generally a good idea to do this, unless there is reason from the context not to do so.

**Diagram 5:3** pictures the relationship asserted in reason *b*, "Buildings are structures."

**Diagram 5:3**

[diagram]

Note that Diagrams 5:2 and 5:3 have a circle in common: the circle for buildings. The diagrams can be combined, drawing the circle for buildings only once, as in **Diagram 5:4**, which you could form by placing Diagram 5:2 over Diagram 5:3.

**Diagram 5:4**

[diagram]

Notice that by combining the diagrams for the two reasons (*a* and *b*), I have made a diagram that shows that the conclusion is inescapable. That is, **Diagram 5:4** shows that the circle for houses is unavoidably inside the circle for structures, which is to say that houses are structures. There is no way to avoid diagramming the conclusion, given the diagrams of the reasons.

### The Basic Circle-System Validity Test

The circle diagram exhibits the validity of the argument of Check-Up Item 5:8. It does this by showing that diagramming the reasons forces us to diagram the conclusion. Here is the circle diagram test for deductive validity:

> Can diagramming the reasons force us to diagram the conclusion? If so, the argument is deductively valid. If not, the argument is deductively invalid.


Apply this test to the next example, Check-Up Item 5:9.

a. Motorcycles are vehicles.
b. Vehicles are mechanical contraptions.
c. Therefore, motorcycles are mechanical contraptions.

Putting the two reasons in the same diagram gives **Diagram 5:5**. You ordinarily do not need to draw two separate diagrams when combining two reasons. One diagram is usually enough:

**Diagram 5:5**

[diagram]

**Diagram 5:5** shows the argument in Check-Up Item 5:9 to be deductively valid. Diagramming the reasons forced me to diagram the conclusion. The circle for motorcycles is unavoidably included in the circle for mechanical contraptions, which is what the conclusion asserts.

Do not be influenced by the relative size of the circles. Relative size is irrelevant. For example, do not infer from **Diagram 5:5** that most mechanical contraptions are vehicles.

Next, I shall show the use of this basic circle system to exhibit deductive invalidity. Check-Up Item 5:10 is an invalid argument:

a. Houses are structures.
b. Homes are structures.
c. Therefore, houses are homes.

**Diagram 5:6** shows this argument to be invalid because it shows that it is possible to diagram the reasons without diagramming the conclusion:

**Diagram 5:6**

[diagram]

I did full justice to the reasons, but managed to avoid diagramming the conclusion. The circle for houses does not need to be inside the circle for homes, as is shown by the upper one of the alternative circles for houses. That shows the argument to be invalid.

The circle for houses could also be in the circle for homes, as is shown by the lower of the alternative circles for houses. This lower circle is not absolutely necessary to show invalidity. But in my experience, most students find that including this sort of thing helps them to feel comfortable with their diagrams.

### Summary

This basic circle system is useful when we are judging the deductive validity of arguments that involve the relationships of classes. A circle represents a class, and a circle within another circle shows that the smaller is included in the larger. If, after drawing the circle relationships for the reasons in an argument in one diagram, we find that we have unavoidably diagrammed the conclusion, the argument is deductively valid. Otherwise, it is not.

The procedure for the basic type of argument we have been considering is first to draw two circles to represent one reason. Then add the other reason to the same diagram, but usually add only one circle because the other circle generally should already be there. This circle for the second reason should go inside or outside the circle that is already there, depending on whether it is included in or includes the other. (They can also overlap and there can be more classes and circles, but those are refinements I shall let you add, if you need to do so.) Then check to see whether the conclusion was also diagrammed and, if so, whether it was unavoidably diagrammed. If it was unavoidably diagrammed, judge the argument deductively valid. If not, it is deductively invalid.

The strategy in diagramming an argument is to keep the conclusion in mind and, giving the reasons every chance to show their power, to try not to diagram the conclusion. If the diagramming of the reasons does not inescapably commit us to diagramming the conclusion, the argument is deductively invalid. The strategy in doing these diagrams is to work against the conclusion, but to be fair to it. We are not trying to represent the world as we know it, but rather to represent the requirements of the reasons as stated, and to see what possibilities are still allowed.

A helpful way to show the deductive invalidity of an argument is to draw alternate circles for a crucial class, with a question mark by the junction of their arrows. One of these circles should be so placed that it denies the conclusion. The other is consistent with the conclusion.

---

## Check-Up 5B

**True or False?**
If false, change it to make it true. Try to do so in a way that shows that you understand.

**5:13** In the circle system, one circle is used to represent a whole proposition.

**5:14** To show that Class A is included in Class B, the circle for A is put inside the circle for B.


**5:15** To represent the proposition *Turtles are egg layers*, the circle for egg layers is put inside the circle for turtles.

**5:16** If a conclusion is unavoidably diagrammed in the diagramming of the reasons, then the argument is deductively valid.

### Short Answer

Diagram each of the following propositions. Label the diagram. Make sure that the points of the arrows touch the circles to which they point.

**5:17** Harleys are motorcycles.

**5:18** Canoes are boats.

**5:19** Basketballs are spheres.

**5:20** Bananas are magnets.

**5:21** Spheres are round objects.

**5:22** Magnets are pieces of fruit.

Here are some deductively valid arguments. Diagram them in a way that shows them to be deductively valid. Label each diagram completely and make sure that the arrow points touch the circles to which they point.

**5:23** 
a. Harleys are motorcycles.
b. Motorcycles are vehicles.
c. Therefore, Harleys are vehicles.

**5:24** 
a. Canoes are boats.
b. Boats are vehicles.
c. Therefore, canoes are vehicles.

**5:25** 
a. Basketballs are spheres.
b. Spheres are round objects.
c. Therefore, basketballs are round objects.

**5:26** 
a. Bananas are magnets.
b. Magnets are pieces of fruit.
c. Therefore, bananas are pieces of fruit.

### Subject Class and Predicate Class

In the proposition "Houses are buildings," the subject class is *houses* because *houses* is the subject of the sentence. The predicate class is *buildings*, and is in the predicate of the proposition. In propositions like this, the circle for the subject class goes inside of the circle for the predicate class because the proposition says that the subject class is included in the predicate class (the "inside–outside" rule). You can see that this is the way it was drawn in **Diagram 5:2**. There are exceptions to this inside-outside rule for drawing circles, so be careful. Make sure that the diagram actually represents what is intended. Use the inside-outside rule for drawing circles only as a temporary crutch.


Sometimes these classes do not explicitly appear in a proposition, so you often have to transform a proposition in order to create explicit classes. Most often, the elusive class is the predicate class, which may be created by changing the predicate to consist of a noun or noun phrase and making sure that either the word *is* or the word *are* is used to connect the two parts of the proposition.

For example, the proposition *Houses are expensive* does not contain a predicate class. There is a subject class, *houses*, but the word *expensive* is an adjective, not the label for a class. So, we make a predicate class, perhaps *expensive things*, and leave the word *are* between the two parts. Thus, you transform *Houses are expensive* into *Houses are expensive things* in order to have two classes connected by an *is* or *are*. The new proposition is diagrammable in the circle system, as you can see:

**Diagram 5:7**

[diagram]

*Birds have wings* is an example of a sentence without an *is* or an *are*. How would you transform that proposition into an *is* or *are* relationship between two classes? Circles inside of circles can explicitly represent only an *is* or *are* relationship, not a *have* relationship.

Here are some possibilities that would work: *Birds are winged creatures*, *Birds are creatures with wings*, *Birds are things that have wings*, and *The bird is a winged creature*. The main problem is to create a predicate class that does justice to the meaning of the original sentence. I like *winged creatures* best, so would diagram *Birds have wings* as follows:

**Diagram 5:8**

[diagram]

Sometimes classes are labeled in such a way that the labels do not look like class labels, such as *the ostrich* and *a bird* in *The ostrich is a bird*. The proposition means the same as *Ostriches are birds*, and is diagrammed in **Diagram 5:9**.

**Diagram 5:9**

[diagram]


Now try to diagram the following argument, which is Check-Up Item 5:11:

**Example 5:6**

a. Birds have wings.
b. The ostrich is a bird.
c. Therefore, the ostrich has wings.

If necessary, rewrite the argument, perhaps as follows:

**Example 5:7**

a. Birds are winged creatures.
b. Ostriches are birds.
c. Therefore, ostriches are winged creatures.

In Example 5:7, each proposition consists of two class terms connected by the word *are*, so the diagram showing the argument to be deductively valid can be made using only nouns (or noun phrases) as labels. This rewriting step is not necessary, as long as you know that it is implied, and as long as you use class terms to label the circles:

**Diagram 5:10**

[diagram]

Note that in order to fit the system, the reasons and the conclusion had to be modified. This is common. You will often have to use your ingenuity.

### Specific Class Members and Universal Terms

The following argument refers to a specific person, Juan:

**Example 5:8**

a. All of the members of the basketball team are tall.
b. Juan is a member of the basketball team.
c. Therefore, Juan is tall.

It does not make sense to represent Juan by a circle because Juan is not a class. We can represent him with an X:


**Diagram 5:11**

[diagram]

Note that a predicate class, *tall people*, had to be created out of the adjective *tall*.

Note also that the words, *all of the*, are left out of the diagramming of the noun phrase, *all of the members of the basketball team*. This is because the circle labeled with "members of the basketball team" automatically represents them all. To say *all* in the diagram would duplicate what is already said by the circle. The boundaries of a circle contain every one of the group or class that is represented by the circle, so words such as *all*, *every*, and *each* are generally omitted from diagrams. The boundaries do the job these words do in the sentences.

### Summary

In attempting to represent a sentence by a circle, we sometimes need to transform the proposition so that it connects exactly two classes, using either the word *is* or the word *are*. Predicate adjectives must be transformed into nouns, and other verbs than *is* or *are* must be changed in a way that captures the meaning of the original proposition. Doing this often makes the result somewhat different from the ways we ordinarily speak, so the result should usually be converted back to ordinary speech.

A member of a class is represented by an X. Universal terms such as *all*, *every*, and *each* are generally left out of diagrams because their meaning is already conveyed by the boundaries of the circles.

If you do not make these transformations—at least mentally—then when things get complex, as they will, confusion will often result.

---

## Check-Up 5C

**True or False?**
If false, change it to make it true. Try to do so in a way that shows that you understand.

**5:27** In a standard class-inclusion proposition, the subject class is represented by the inner circle.

**5:28** Putting one circle inside another indicates that the class represented by the inner circle is included in the class represented by the outer circle.

**5:29** Before diagramming a proposition like *chairs can burn*, one must at least mentally transform the proposition into a proposition composed of two classes (represented by nouns or noun phrases) connected by the word *is* or the word *are*.

**5:30** The proposition *Grasshoppers are flying creatures* is in the recommended idealized form, ready to be diagrammed.

**5:31** The subject of the proposition *All office chairs are uncomfortable* is represented in a diagram by the words *office chairs*, the word *all* being omitted.

**Short Answers**
Here are some propositions to practice diagramming. Diagram each and label the parts in full with nouns or noun phrases. Make sure that the arrows touch the circles.

**5:32** All the chairs in this room are wooden.

**5:33** All wooden things can burn.

**5:34** Raoul plays soccer.

**5:35** All soccer players are in good physical shape.

Here are some more deductively valid arguments. Diagram them (using circles) in a way that shows them to be deductively valid. Label the diagrams completely.

**5:36** 
a. All parallelograms are quadrilaterals.
b. All quadrilaterals are plane figures.
c. Therefore, all parallelograms are plane figures.

**5:37** 
a. All the chairs in this room are wooden.
b. All wooden things can burn.
c. Therefore, all the chairs in this room can burn.

**5:38** 
a. Raoul plays soccer.
b. All soccer players are in good physical shape.
c. Therefore, Raoul is in good physical shape.

**5:39** 
a. *Magic Mountain* is by Thomas Mann.
b. All of Thomas Mann's books are good.
c. Therefore, *Magic Mountain* is a good book.

The following deductively valid arguments are written in more natural form. For each, (a) state the conclusion and (b) make a circle diagram of the argument to show it to be deductively valid. Make sure that the diagram is properly labeled.

**5:40** All mayors are politicians. Nobody can doubt that. Furthermore, all politicians are deeply concerned about taxes. Therefore, all mayors are deeply concerned about taxes.

**5:41** Because Sarah Washington is a mayor, and all mayors are deeply concerned about taxes, it must be true that Sarah Washington is deeply concerned about taxes.

**5:42** All literary works that have fascinated me have had an influence on my life. Because all of Chekhov's short stories have fascinated me, they have all had an influence on my life.


**5:43** All unwanted plants are weeds. We do not want the wheat in our corn field. Therefore, those wheat plants are weeds.

**5:44** Anything that interferes with people's desires is unjust. Because zoning interferes with people's desires, it is certainly unjust.

**5:45** Anything that promotes the good life is just. Because zoning promotes the good life, it is just.

### Exclusion

Just as class inclusion is represented by one circle inside another, class exclusion is represented by two completely separate circles. For example, the proposition *No vehicles are permitted* could be represented this way:

**Diagram 5:12**

[diagram]

**Diagram 5:12** says that the class of vehicles is *excluded* from the class of things that are permitted. Now try to diagram the argument of Example 5:9, which you have seen as Check-Up Item 5:12:

**Example 5:9**

a. No vehicles are permitted.
b. Motorcycles are vehicles.
c. Therefore, no motorcycles are permitted.

Try to diagram Example 5:9 before you read further.

**Diagram 5:13** exhibits the deductive validity of Example 5:9:

**Diagram 5:13**

[diagram]

In drawing **Diagram 5:13**, I first drew the first reason by drawing two separate circles: one for vehicles and one for things that are permitted. Then I drew the circle for motorcycles inside the circle for vehicles, as required by the second reason. This unavoidably put the circle for motorcycles totally separate from the circle for things that are permitted, which is what the conclusion says. Therefore, the conclusion is inescapably diagrammed by diagramming the reasons, so the argument is deductively valid.


### Nonmembership

Like exclusion, nonmembership is shown by putting the X for an individual outside of a circle. See **Diagram 5:14** for one way to diagram the proposition *Joan's bike is not permitted*.

**Diagram 5:14**

[diagram]

In Example 5:10, the proposition diagrammed in **Diagram 5:14**, *Joan's bike is not permitted*, is the conclusion:

**Example 5:10**

a. No motorcycles are permitted.
b. Joan's bike is a motorcycle.
c. Therefore, Joan's bike is not permitted.

As shown by **Diagram 5:15**, this conclusion is inescapable, given the reasons, so the argument is deductively valid.

**Diagram 5:15**

[diagram]

### Invalid and Valid: Terms of Condemnation and Commendation

In deductive logic books and courses, it is common practice to use the words *invalid* and *valid* without their being preceded by the word *deductively*. This practice is confusing to many people because in everyday speech, *invalid* by itself is a general term of condemnation of arguments and statements, and *valid* by itself a general term of commendation. So, it will seem to many people that, when these words are used, general commendation or condemnation is claimed. If so, and the word *deductively* is not used, it might then seem that we are invited to condemn all *deductively* invalid arguments, even if they are good arguments (like the prosecutor's and the pathologist's). It might also seem that we are invited to commend deductively valid but circular arguments (arguments that make no progress), and deductively valid arguments that have false reasons and that are offered in support of their conclusions. These invitations should be refused.

To avoid confusion in deductive logic, I place the word *deductively* in front of the words *invalid* and *valid* (unless I actually do mean general condemnation or commendation). I urge you to do likewise, even though it is sometimes more convenient to omit the word *deductively*. Deductive validity is not automatic success and deductive invalidity is not automatic failure.

### Summary and Comment

Class exclusion is represented by drawing circles separate from each other. Similarly, nonmembership can be represented by placing the X for the nonmember outside of the circle for the class of which it is not a member.

Because *valid* and *invalid* are in everyday speech taken to be general words for commendation and condemnation of arguments, it is best to attach the word *deductively* to them when we are talking about deductive validity and invalidity. Otherwise, confusion can result.

There are many other refinements for the circle system, including using overlapping circles.[^3] But this introduction should get you started. Develop your own adaptations of these ideas. No system will answer all questions. You need to ask yourself continuously, "Does what I am doing make sense in this situation?"

---

## Check-Up 5D

**True or False?**
If false, change it to make it true. Try to do so in a way that shows that you understand.

**5:46** Class exclusion can be represented by drawing two circles separated from each other.

**5:47** Class nonmembership can be shown by drawing an X inside the class of which the individual is not a member.

**5:48** You will sometimes need to make adaptations of the presented circle system to fit your situation.

**5:49** If it is possible to diagram the reasons without diagramming the conclusion, then the argument is deductively invalid.

**5:50** In diagramming an argument, if it is possible to avoid diagramming the conclusion, then you must show this possibility.

[^3]: For some possibilities, see R. L. Armstrong and L. W. Howe, "An Euler Test for Syllogisms," *Teaching Philosophy*, 13 (1) (March 1990), pp. 39–46; James O. Bennett and John Nolt, "Venn/Euler Test for Categorical Syllogisms," *Teaching Philosophy*, 17 (1) (March 1994), pp. 41–55; Keith Stenning and John Oberlander, "A Cognitive Theory of Graphical and Linguistic Reasoning: Logic and Implementation," *Cognitive Science*, 19 (1995), pp. 97–140; and my *Natural Language Logic*, forthcoming.


**5:51** If it is possible to diagram the conclusion, then the argument is deductively valid.

**5:52** Any argument that is deductively valid is a good argument.

**5:53** Any argument that is deductively invalid is a bad argument.

**5:54** In this book, the word *valid* means *deductively valid*.

**5:55** Using *invalid* to mean *deductively invalid* can be confusing to most people.

### Short Answer

For each of the following deductively valid arguments, (a) state the conclusion and (b) draw a diagram of the argument that shows it to be deductively valid, making sure that the labels are perfectly clear.

**5:56** No dogs are permitted in the park. Because Mike is a dog, he is not permitted in the park.

**5:57** No leaded gasoline is permitted in this fuel tank. Therefore, the gasoline from this can is not permitted in this tank because the gasoline from this can is leaded gasoline.

**5:58** Nobody under thirty-five years of age can be president. Because Tina is under thirty-five years of age, she cannot be president.

**5:59** Twenty-year-olds are not eligible to vote. Mirabelle is twenty, so she is ineligible to vote.

**5:60** It is clear that Sharon will have to pay the full admission price. This is because she is over eleven, and nobody over eleven does not pay the full admission price.

**5:61** Henry, on the other hand, will not pay the full admission price because he is eleven, and nobody who is eleven (or under) pays the full admission price.

**5:62** Nothing written by that bureaucrat makes any sense. Because Regulation EZCOMP will be written by that bureaucrat, it will not make any sense.

**5:63** The canteen is not open today. I am sure of this because no stores are open today and

[An additional challenge for you in this item is to fill in a reason that would make the argument deductively valid. Identifying this likely assumption gives you a glimpse of this activity, which is discussed in Chapter 7.]

### More Short Answer

For each of the following arguments, (a) state the conclusion and (b) make and label a diagram that shows the argument to be deductively invalid. As a reminder of a way to exhibit deductive invalidity, the first is done as an example.

**5:64** Alligators are vertebrates that live in and out of water. But we know very well that amphibians are vertebrates that live in and out of water. Therefore, alligators are amphibians.


a. Conclusion: Alligators are amphibians
b. [diagram]

**5:65** People under eighteen are not permitted to vote. Because Mark is not permitted to vote, he is under eighteen.

**5:66** All good communists are opposed to the reelection of the governor. Because the members of the action committee are opposed to the reelection of the governor, the members of the action committee are good communists.

**5:67** Nobody in the in-group rides a three-speed bicycle. Nobody who rides a three-speed bicycle is careless with our energy supply. From this we can see that nobody in the in-group is careless with the energy supply.

**5:68** People who think critically are in favor of the new zoning law. From this, it follows that the members of the planning commission are critical thinkers because they are unanimously in favor of the new zoning law.

**5:69** Propositions that have been proved beyond a reasonable doubt are true. Because the proposition that the defendant was not justified in using the force she used has not been proven beyond a reasonable doubt, that proposition is not true. (Hint: Use types of propositions for your classes, such as *true propositions* and *propositions that have been proven beyond a reasonable doubt*.

### More Short Answer

For each of the following arguments, (a) state the conclusion, (b) make a labeled circle diagram of the argument exhibiting whether it is valid or invalid, and (c) report your judgment with the words *deductively valid* (or *DV*) or *deductively invalid* (or *DI*).

**5:70** All squares have four right angles. Figure ABCD is a square. Therefore, figure ABCD has four right angles.

**5:71** All nearsighted people have difficulty seeing things far away. John has difficulty seeing things far away. Therefore, he is nearsighted.

**5:72** Birds that are unable to fly are fast runners. The penguin is a bird that is unable to fly. From this it follows that the penguin is a fast runner.

**5:73** Indices used to show trends in productivity should take into account changes in the cost of living. The percent increase in the Gross Domestic Product is an index used to show trends in productivity. Therefore, that index should take into account changes in the cost of living.

**5:74** The first few sentences in Marc Antony's speech to the people of Rome should be combined because these sentences are short, and short sentences should always be combined.

**5:75** The practice of lay investiture weakened the church. Practices weakening the church were opposed by the papacy. Therefore, there is no doubt that the practice of lay investiture was opposed by the papacy.

**5:76** An equilateral polygon inscribed in a circle is a regular polygon. ABCDE is a regular polygon. From this we know that ABCDE is an equilateral polygon inscribed in a circle.

**5:77** Electric bells in complete circuits ring loudly. The front doorbell is in a complete circuit. Therefore, although we cannot hear it from here, it must be ringing loudly.

**5:78** People who are not trusted by the American people are not elected president. Marguerite Blank is trusted by the American people. Therefore, she will win the presidential election.

**5:79** Blaine was not trusted by the American people. This fact follows from the fact that the American people do not elect people whom they do not trust and the fact that they did not elect him.

**5:80** Complementary colors are pairs of colors that, when combined, appear to be white. Blue and yellow are a pair of complementary colors. From this, you can predict that blue and yellow, when combined, will appear to be white.

**5:81** Let us assume that plants and animals that are not closely related cannot be crossed to produce hybrids. Because the two species that we have been studying (let us call them *X* and *Y*) are closely related, they can be crossed to produce hybrids.

**5:82** I have concluded that Mary does not know the rules of punctuation. Here's why: People who know the rules of punctuation do well in their written compositions. But Mary does not do well in her written composition, so my conclusion follows.

**5:83** All heretics were condemned, but no true believers were heretics. Therefore, no true believers were condemned.

**5:84** "... none of woman born shall harm Macbeth." But "Macduff was from his mother's womb untimely ripp'd." Therefore, Macduff shall harm Macbeth.

## Suggested Answers for Chapter 5

*Note:* Different diagrams from those suggested are often at least as good as the ones given. If yours differ from the ones suggested, then either try to satisfy yourself that yours are all right, or figure out why not.

### Check-Up 5A

5:1 T  5:2 T  5:3 F  5:4 F  5:5 F  5:6 T  5:7 T

5:3 Deductive validity is not equivalent to proof beyond a reasonable doubt; the inference part of deductive validity is more demanding, but the establishment of the reasons part is much less demanding—actually not demanding at all.

5:4 Deductively invalid arguments can have true conclusions.

5:5 Deductively valid arguments can have false conclusions when they have false reasons.

5:8 Deductively valid

5:9 Deductively valid

5:10 Deductively invalid

5:11 Deductively valid

5:12 Deductively valid

### Check-Up 5B

5:13 F  5:14 T  5:15 F  5:16 T

5:13 In the circle system, propositions are represented by circles and Xs.

5:15 To represent the proposition *Turtles are egg layers*, the circle for turtles is put inside the circle for egg layers.

5:17 [diagram]

5:18 [diagram]

5:19 [diagram]

5:20 [diagram]

5:21 [diagram]

5:22 [diagram]

5:23 [diagram]

5:24 [diagram]

5:25 [diagram]

5:26 [diagram]


### Check-Up 5C

5:27 T  5:28 T  5:29 T  5:30 F  5:31 T

5:30 The proposition *Grasshoppers are flying creatures* is in the recommended idealized form, ready to be diagrammed.

5:32 [diagram]

5:33 [diagram]

5:34 [diagram]

5:35 [diagram]

5:36 [diagram]

5:37 [diagram]

5:38 [diagram]

5:39 [diagram]

5:40 
a. Conclusion: All mayors are deeply concerned about taxes.
b. [diagram]

5:41 
a. Conclusion: Sarah Washington is deeply concerned about taxes.
b. [diagram]

5:42 
a. Conclusion: All Chekhov's short stories have had an influence on my life.
b. [diagram]

5:43 
a. Conclusion: Those wheat plants are weeds.
b. [diagram]

5:44 
a. Conclusion: Zoning is unjust.
b. [diagram]

5:45 
a. Conclusion: Zoning is just.
b. [diagram]

### Check-Up 5D

5:46 T  5:47 F  5:48 T  5:49 T  5:50 T  5:51 F

5:52 F  5:53 F  5:54 F  5:55 T

5:47 Class nonmembership can be shown by drawing an X outside the class of which the individual is not a member.

5:51 The *possibility* of diagramming the conclusion does not ensure deductive validity.

5:52 Good arguments need not be deductively valid.

5:53 Some good arguments are deductively invalid.

5:54 In this book and in everyday language, the word *valid* by itself does not mean *deductively valid*.

5:56 
a. Conclusion: Mike is not permitted in the park.
b. [diagram]

5:57 
a. Conclusion: The gasoline from this can is not permitted in this tank.
b. [diagram]

*Note:* The gasoline from this can could have been represented with an *X* instead of a circle. It does not matter.

5:58 
a. Conclusion: Tina cannot be president.
b. [diagram]

5:59 
a. Conclusion: Mirabelle is ineligible to vote.
b. [diagram]

5:60 
a. Conclusion: Sharon will have to pay the full admission price.
b. [diagram]

5:61 
a. Conclusion: Henry will not have to pay the full admission price.
b. [diagram]

5:62 
a. Conclusion: Regulation EZCOMP will not make any sense.
b. [diagram]

5:63 
a. Conclusion: The canteen is not open today.
b. [diagram]
c. Unstated reason, or assumption: The canteen is a store.


5:64 Done in text as an example.

5:65 
a. Conclusion: Mark is under eighteen.
b. [diagram]

5:66 
a. Conclusion: The members of the action committee are good communists.
b. [diagram]

5:67 
a. Conclusion: Nobody in the in-group is careless with the energy supply.
b. [diagram]

5:68 
a. Conclusion: The members of the planning commission are critical thinkers.
b. [diagram]

5:69 
a. Conclusion: The proposition that the defendant was not justified in using the force she used is not true.
b. [diagram]


5:70 
a. Conclusion: Figure ABCD has four right angles
b. [diagram]
c. DV

5:71 
a. Conclusion: John is nearsighted.
b. [diagram]
c. DI

5:72 
a. Conclusion: The penguin is a fast runner.
b. [diagram]
c. DV

5:73 
a. Conclusion: The percent increase in the Gross Domestic Product is an index that should take into account changes in the cost of living.
b. [diagram]
c. DV


5:74 
a. Conclusion: The first few sentences in Marc Antony's speech to the people of Rome should be combined.
b. [diagram]
c. DV

*Henceforth in this set, odd-numbered answers will be omitted. A challenge!*

5:76 
a. Conclusion: ABCDE is an equilateral polygon inscribed in a circle.
b. [diagram]
c. DI

5:77 Deliberately omitted.

5:78 
a. Conclusion: Marguerite Blank will win the presidential election.
b. [diagram]
c. DI

5:79 Deliberately omitted.

5:80 
a. Conclusion: Blue and yellow, when combined, will appear to be white.
b. [diagram]
c. DV


*Note:* For convenience, I treated *blue* and *yellow* together as a member of the class, *pairs of colors*. I hope you were able to extend the system in a way that enabled you to handle this situation in a reasonable way. You will have to do this sort of thing in the future because no system answers all the questions. You often have to be creative and sensitive in dealing with practical situations.

5:81 Deliberately omitted.

5:82 
a. Conclusion: Mary does not know the rules of punctuation.
b. [diagram]
c. DV

5:83 Deliberately omitted.

5:84 
a. Conclusion: Macduff shall harm Macbeth.
b. [diagram]
c. DI

*Thought question:* What then does follow?