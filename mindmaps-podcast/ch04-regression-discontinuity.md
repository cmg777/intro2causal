# Regression discontinuity: a podcast companion to the mind map

Two voices: HOST, a curious student, and ECONOMIST, a friendly econometrics teacher.

## Opening

HOST: Welcome back. Today we are on regression discontinuity, and a birthday with serious consequences. Legal access to alcohol changes suddenly at a particular age. Human bodies do not suddenly become different. Could that contrast teach us something about deaths among young adults?

ECONOMIST: That is the starting point. Researchers studying American mortality found a clear increase around the legal drinking birthday. Their question was whether access to alcohol caused that increase. Simply comparing drinkers with people who avoid alcohol would not settle it. Those groups may differ in risk taking, health, and many other ways.

HOST: So our question is: Does legal access to alcohol raise death rates? We need a comparison that does more than show drinking and danger together.

ECONOMIST: By the end of this episode, you should be able to explain how a cutoff creates a causal comparison. You should also distinguish sharp from fuzzy regression discontinuity. Finally, you should evaluate the assumptions and limits of an estimated jump. We will use the drinking age and Boston's selective schools to practice those skills.

HOST: Our mind map takes us through The Question, The Investigation, and The Resolution. I like the idea of a rule creating an experiment. But I am suspicious. If a rule determines everything, where does a fair comparison come from?

ECONOMIST: Keep that suspicion. It will help. The rule itself is not random. Instead, we compare people extremely close to where it changes. We ask whether their expected outcomes would otherwise join smoothly. If that condition is credible, a sudden outcome change becomes informative. If it fails, the same apparent jump can mislead us.

## Part 1: The Question

HOST: Let us enter The Question. Start with legal access rather than actual drinking. Why is that distinction so important? An underage person can still find alcohol, while someone above the legal age can choose to avoid it.

ECONOMIST: The treatment in our first design is permission to obtain alcohol legally. In the American setting studied, that permission begins at 21. It does not mean everyone suddenly drinks. It means the legal restriction switches. The causal effect includes the behavioral response to that change. It is an effect of access, not the biological effect of drinking a fixed amount.

HOST: Other eligibility rules have that same structure. The study guide mentions voting at 18 and Medicare eligibility at 65. They sound like promising places to look. But the rule alone cannot guarantee that an outcome change comes from the policy we care about.

ECONOMIST: Exactly. Those are examples of thresholds, not completed causal studies. Each application needs its own investigation. For alcohol, the policy debate matters. Supporters of a lower drinking age argued that earlier legal access could encourage more responsible drinking. Others believed restricting access prevented harm. We should judge these arguments using evidence, rather than assuming either story must be right.

HOST: My first prediction is that if birthdays alone create dangerous celebrations, deaths should rise around neighboring birthdays too. Would that weaken the argument that legal drinking access matters?

ECONOMIST: The birthday comparison gives a useful reveal. The original study discussion finds a distinctive spike around the legal drinking birthday. Neighboring birthdays do not show the same pronounced pattern. That weakens a generic birthday explanation. But it does not yet answer whether the increase persists beyond a brief celebration. We need a broader comparison around the threshold.

HOST: Here is the puzzle of rigid rules. A person just short of the birthday and someone just past it can be nearly the same age. Yet their legal access differs completely. The comparison gets interesting precisely because the rule changes abruptly.

ECONOMIST: Yes. Think of age advancing gradually, while eligibility changes suddenly. We do not claim nearby people are identical in every detail. We need their average underlying risks to vary smoothly. The mortality data grouped by month of age show more than a single birthday spike. They suggest a step upward around the legal boundary. That pattern motivates the design.

HOST: What does smoothly mean here? Are you saying the death rate must stay constant as people grow older? That seems unlikely, especially when young people are gaining experience and changing their behavior.

ECONOMIST: Smoothly does not mean constant. Mortality may rise, fall, or curve with age. The requirement concerns a sudden break at the exact boundary. Without the legal change, the expected outcome should approach the same value from either side. A gradual improvement in road safety with maturity is compatible with that condition. An unrelated policy starting on the same birthday would create a problem.

HOST: Let us build the vocabulary before we fit anything. Regression discontinuity is a long name. Can we unpack the words and give every moving part a simple job?

ECONOMIST: We will call it RD after this. The running variable is the measure that determines eligibility. Here it is age. The cutoff is the boundary in that measure. The treatment indicator records whether legal access is switched on. Discontinuity means a break or jump. Regression describes the statistical method used to separate that jump from the surrounding trend.

HOST: And sharp versus fuzzy describes what happens to treatment at the boundary? I want to avoid confusing a sharp legal rule with a claim that everyone follows it perfectly.

ECONOMIST: Correct. In sharp RD, the treatment being studied switches completely at the cutoff. Legal access is sharp even though drinking behavior is not. In fuzzy RD, the chance or intensity of the treatment changes, without a complete switch. A school offer might increase attendance without determining it. We must define the treatment before choosing the label.

HOST: We also need continuity, bandwidth, and placebo tests. I can remember the first as the smooth comparison we would expect without treatment. What do the other terms add?

ECONOMIST: Bandwidth tells us how far from the boundary we include observations. A narrow bandwidth uses only close neighbors. A placebo test asks whether something that should remain unchanged also jumps. For example, disease deaths can help test the alcohol story. These tools examine the design. They do not make its assumptions disappear.

HOST: Let me recap The Question. Legal access changes abruptly, while ordinary age related risks should change gradually. We will compare close neighbors, distinguish access from drinking, and test whether a jump deserves a causal interpretation.

ECONOMIST: That is our foundation. Nearness creates an opportunity, not an automatic experiment. Next we must explain precisely what we compare, how we estimate it, and what could make us wrong.

## Part 2: The Investigation

HOST: We now enter The Investigation. Our first obstacle is no overlap at the threshold. At a given exact age, everyone faces the same legal rule. Where do we find an untreated comparison for someone who is already eligible?

ECONOMIST: We cannot find it at that exact age. That makes RD different from ordinary regression comparisons within the same control group. Instead, we estimate the outcome trend below the boundary and continue it toward the boundary. We also estimate the trend above it. We compare their predicted values where the rule switches. This short continuation of a trend is called extrapolation.

HOST: So saying that we simply control for age hides the central challenge. There is no exact age with both legal conditions in the data. We are trusting a relationship across nearby ages, rather than comparing eligible and ineligible people of identical age.

ECONOMIST: Precisely. Imagine asking what mortality would have been just above the boundary if access had remained restricted. That unobserved alternative is the counterfactual. The trend just below the boundary helps estimate it. The justification comes from continuity near the boundary. A regression formula alone cannot supply that justification.

HOST: Now the sharp design can be stated carefully. The running variable is age, the cutoff is 21, and the legal access indicator is the switch. Are the probabilities at this boundary literally changing from 0 to 100 percent?

ECONOMIST: For the legal access indicator, yes. Those figures describe eligibility, not drinking participation. The identifying assumption concerns potential outcomes, meaning the outcomes under each possible legal regime. Around the boundary, those underlying outcome relationships must be continuous. Then an abrupt difference in observed mortality can be attributed to the change in access.

HOST: My prediction for this part is that a smooth downward age trend does not rule out harm from access. Mortality could be falling on both sides, while still stepping upward at the boundary. Is that what happens?

ECONOMIST: That prediction is right. The book's mortality comparison shows generally declining death rates with age among these young adults. At the legal drinking boundary, the fitted mortality level steps upward. A falling background trend and a harmful policy effect can coexist. Comparing broad averages across ages could obscure that distinction.

HOST: Now explain the RD regression tool without asking us to read an equation. What should the computer separate, and why should we examine the underlying data before trusting its answer?

ECONOMIST: The simple model separates a baseline level, an age trend, and a jump when legal access begins. The age trend captures gradual change. The jump measures the additional change at the boundary. Plotting first helps reveal unusual observations, curvature, or a result that exists only because the fitted model forces it. An attractive coefficient cannot repair a poor fit.

HOST: If the model uses separate fitted lines, are their slopes always different? The map's simple equation sounds as though it has just one age trend, yet its explanation mentions a line on each side.

ECONOMIST: Good distinction. The simplest specification imposes the same slope on both sides, while allowing a level change. That creates parallel fitted lines. A more flexible specification lets the slopes differ. Either way, the effect of interest is the separation evaluated at 21. Comparing their heights far away would require additional extrapolation.

HOST: Why do researchers sometimes recenter age around the cutoff? Does changing the starting point change any actual comparison, or is it only a way to keep the interpretation clear?

ECONOMIST: It keeps interpretation clear. We measure distance from the boundary rather than age from birth. At the boundary, that distance vanishes. When we allow different slopes, the coefficient representing the level jump therefore still measures the gap exactly at the threshold. Rewriting the same fitted relationship this way does not create new evidence.

HOST: Let us examine the mortality case itself. The observations are monthly age groups, rather than a separate regression record for every individual. What exactly is measured, and what does the estimated jump mean?

ECONOMIST: Each monthly group has an annual death rate per 100,000 people. Monthly describes the age grouping, not the time unit of the reported mortality rate. The broad sample covers ages 19 through 22, extending up to the next birthday. The simple linear estimate adds about 7.7 annual deaths on that same population scale near the legal boundary.

HOST: I want to work through the scale. The book describes an average death rate around 95, and the extra rate is about 7.7. To express the increase relative to that average, I divide the extra rate by the average rate, then multiply by 100. What do we get?

ECONOMIST: That gives about 8.1 percent. This calculation uses the book's approximate average as the denominator. It is not the share of all young people who die because of access. The absolute increase remains extra annual deaths per 100,000 people. The relative figure helps judge its size against the mortality rate in this sample.

HOST: That distinction matters. A rate increase can be important without meaning that a large percentage of the entire population dies. What kinds of deaths account for the jump? A plausible mechanism should help us assess the alcohol explanation.

ECONOMIST: Motor vehicle fatalities account for much of it. The estimates are roughly between 4 and 6 extra annual deaths per 100,000, depending on the specification. The results also suggest increases in suicide and some other external causes. Direct alcohol poisoning contributes less. The main concern is not simply poisoning from the drink itself, but harm linked to behavior after drinking.

HOST: Disease deaths are the proposed placebo. If cancer and heart disease suddenly increased at this exact birthday too, I would worry about the comparison or the data. Do those internal causes actually stay flat?

ECONOMIST: The broad sample gives small, statistically uncertain estimates for internal causes. That supports the access interpretation, since these deaths should not respond immediately in the same way. But we should soften the map's blanket claim of no jump. In one narrower specification, the internal cause estimate is distinguishable from zero at conventional levels. The check is supportive overall, not flawless in every version.

HOST: Does that exception destroy the whole study, or should it change how confidently we describe the evidence? It sounds like the difference between taking a diagnostic seriously and demanding a perfectly quiet dataset.

ECONOMIST: We should report the exception and consider the pattern across outcomes and specifications. Chance can produce isolated results, while a systematic failure would be more troubling. The motor vehicle evidence fits the causal story particularly well. No individual placebo guarantees validity. Together, the design, the outcome pattern, and the robustness checks build the argument.

HOST: The robustness toolkit comes next. A smooth curve can look like a step if we insist on fitting straight lines. How do we avoid manufacturing a discontinuity from the wrong trend?

ECONOMIST: We try reasonable alternatives and report them. A quadratic trend allows curvature, meaning the slope can change gradually. Interacting the age terms with eligibility allows different curvature on each side. These choices can describe the data better, but flexibility is not automatically truth. We should ask whether the important conclusion survives credible changes, rather than choosing the version with our favorite result.

HOST: Bandwidth changes address the same concern differently. The map contrasts a broad group beginning at 19 with a narrower window from 20 to 22. Can you make the endpoints and the tradeoff clear?

ECONOMIST: The broad window includes the completed ages through 22, approaching the next birthday. The narrow window is within about a year on either side of the cutoff. In the table's completed age labels, it covers ages 20 and 21. Closer observations leave less room for misleading curvature. But fewer observations make the estimated jump less precise.

HOST: So the apparent disagreement between completed age labels and continuous age endpoints is mostly notation. The real statistical decision is how far we reach on either side. Does the all cause result survive those changes?

ECONOMIST: Across the table's linear and flexible models, and its broad and narrow windows, the jump is roughly between 7 and 10 extra deaths per 100,000. The flexible broad sample estimate is about 9.5. Those are not identical results, but their shared direction and similar magnitude are reassuring. They are evidence of stability, not proof against every possible bias.

HOST: Is the narrowest possible window always best? If close neighbors make the comparison more credible, it is tempting to keep discarding observations until we are almost exactly at the cutoff.

ECONOMIST: Then uncertainty may become enormous. This is the bias and variance tradeoff. Bias means systematic distortion, such as forcing the wrong trend. Variance describes sampling noise. A narrower window can reduce trend bias while increasing noise. Methods can help choose a bandwidth, but judgment remains. Researchers should show that findings do not depend on one convenient choice.

HOST: The book also contrasts parametric and nonparametric approaches. Those labels sound more different than the actual reasoning. Are both still trying to estimate what happens near the same boundary?

ECONOMIST: Yes. Parametric methods specify a trend over a chosen range, such as a line or curve. Nonparametric RD focuses on a neighborhood and often fits local lines there. Local means close to the boundary. It may give closer observations more weight. Neither approach is free of choices. Both must separate a genuine break from smooth variation and report uncertainty.

HOST: We are ready for the fuzzy extension. A cutoff might change the chance of receiving treatment without determining everyone's behavior. How does the reasoning change when the switch is incomplete?

ECONOMIST: First estimate the jump in outcomes at the cutoff. This is the reduced form, the effect of crossing the eligibility boundary on the outcome. Then estimate the jump in treatment receipt or intensity. This is the first stage. Dividing the outcome jump by the treatment jump scales the eligibility effect into an effect of treatment.

HOST: That sounds like instrumental variables from our earlier episode. The cutoff becomes an instrument, a source of treatment variation we hope is unrelated to the other causes of the outcome. Is that the connection?

ECONOMIST: Exactly. Two stage least squares is a way to carry out that instrumental variables calculation. The first stage predicts treatment using the cutoff indicator and suitable running variable controls. The second uses the predicted treatment, keeping those same controls. The eligibility indicator is excluded from that second relationship because it supplies the identifying variation.

HOST: Dividing two jumps is easy arithmetic. Giving the ratio a causal meaning is harder. What assumptions must survive when a sharp eligibility rule produces only a fuzzy change in actual treatment?

ECONOMIST: The first stage must be meaningful, and the continuity comparison must still hold. The exclusion restriction says crossing the boundary affects the outcome through the specified treatment. For binary treatment, a further monotonicity condition rules out people whose treatment moves in the opposite direction because eligibility improves. Under those conditions, the ratio identifies a local effect for compliers, the people whose treatment changes because of eligibility.

HOST: And with treatment intensity, such as the achievement level of classmates, we should not automatically call the ratio the effect for every student. We must say what changes and which causal interpretation our model supports.

ECONOMIST: Right. A continuous exposure requires more care than a simple attendance switch. The estimated effect scales an outcome change by the exposure change induced at this boundary. Its interpretation depends on assumptions about that exposure and its effects. Sharp RD also has assumptions; ordinary least squares is merely an estimation tool. Neither label is a certificate of causality.

HOST: Now Boston's exam schools give us a concrete fuzzy case. Selective schools have impressive students, but admitting high achievers can create impressive averages even if the school adds little. What comparison avoids confusing those possibilities?

ECONOMIST: Compare applicants close to an admissions cutoff. The chapter focuses on Boston Latin School. Its running variable combines an entrance examination score with earlier school grades. The book often calls it the exam score for short. Qualification creates a large jump in enrollment there, but some qualifying students go elsewhere. Crucially, most applicants just missing this cutoff attend another selective exam school.

HOST: Then this is not simply selective school against ordinary school. If many students on both sides attend an exam school, their educational environments differ more subtly. What treatment actually changes sharply enough to study?

ECONOMIST: Their classmates' prior achievement changes. Qualifying students encounter peers with substantially stronger earlier math scores. The estimated jump is about 0.8 standard deviations. A standard deviation measures how spread out scores are. This peer measure uses schoolmates' scores from before admission. It therefore describes the entering peer group rather than an outcome created by the new school.

HOST: My intuition says stronger classmates should improve learning. A simple association supports that intuition. But similar families and earlier opportunities could help both students and their classmates. Does the cutoff change applicants' own earlier achievement too?

ECONOMIST: The chapter reports no comparable jump in applicants' earlier scores or measured background characteristics. That supports a comparison between similar applicants facing different peer environments. Yet the later math outcome does not show a clear corresponding increase. The reduced form estimate is slightly negative and uncertain. We should say no clear achievement gain was detected, rather than declaring the true effect exactly zero.

HOST: That is a useful correction to the map's shorthand that achievement does not jump. The absence of a statistically clear gain still leaves uncertainty. And it concerns marginal applicants near this particular boundary, compared with their actual alternatives.

ECONOMIST: Yes. The book's instrumental variables estimate for peer achievement is also near zero and uncertain. But there is a further caveat. Admission may change teachers, courses, and the racial composition of classmates as well as peer achievement. A pure peer effect interpretation requires those other channels to have no direct effect on the measured outcome. That exclusion restriction is demanding.

HOST: Could we just choose a different channel, such as classmates' racial composition, and repeat the division? Would that let us discover which feature matters most?

ECONOMIST: The same small outcome jump would produce a small ratio for any exposure with a substantial first stage. That arithmetic cannot distinguish the channels. The book argues that other beneficial school features might make the peer estimate too positive, making the small result striking. That argument depends on the direction of those other effects. It does not prove every channel is absent.

HOST: What is a responsible policy implication for school choice? Parents may value many things besides the particular math scores measured here. A policymaker should be cautious about turning a local comparison into a judgment about every selective school.

ECONOMIST: Exactly. The findings challenge the claim that impressive school averages reveal large causal gains from attending. They do not show that schools never matter, or that every admission policy has the same effect. The measured outcomes, applicants near the cutoff, competing schools, and multiple treatment channels all define the scope of the evidence.

HOST: Let us finish the investigation with interpretation and roots. We have repeatedly said local effect. Why does a convincing comparison near the boundary tell us less about people far away from it?

ECONOMIST: Because their untreated outcomes require a much longer extrapolation. The mortality evidence concerns access near the legal drinking age in a society where older adults already have access. It cannot directly predict national prohibition or access for much younger children. The book considers effects farther from the boundary, but explicitly treats them as more speculative. A fitted curve can extend farther than our causal confidence.

HOST: This approach has a surprisingly long history. The map names Thistlethwaite and Campbell in 1960, studying National Merit recognition. Their question was whether recognition itself changed students' plans, rather than whether recognized students already differed from everyone else.

ECONOMIST: Comparing students around the recognition cutoff gave a different answer from a simple selection driven comparison. The estimated difference in career plans was small and statistically uncertain. That early application demonstrates the same principle as Boston's schools. A visible badge of success and a later outcome can be associated without the badge causing the outcome.

HOST: Here is our recap of The Investigation. We estimated trends on either side, separated the jump, checked alternative models and windows, and examined causes of death. Then fuzzy RD used a treatment jump to interpret an eligibility effect. Both cases required assumptions and careful limits.

ECONOMIST: And the most important habit was defining the actual comparison. Legal access differs from drinking. A school offer differs from attendance. Boston Latin differs from the alternative schools students actually attend. Clear treatment definitions turn a numerical result into a meaningful causal answer.

## Part 3: The Resolution

HOST: We have reached The Resolution, starting with the devil's advocate. My objection is that RD just controls for the running variable. Why give it a special name when regression already lets us add age or test scores?

ECONOMIST: Because the source of identification differs. With ordinary controlled comparisons, we hope treated and untreated people can be compared at the same control values. In sharp RD, the rule prevents that overlap. We instead rely on continuity and extrapolate toward a boundary. How we describe the trend therefore matters directly to the causal claim. The special name reminds us of that special argument.

HOST: Here is my prediction for the last part. If another policy changes at the same birthday, a mortality jump alone cannot tell us which policy caused it. Even an extremely precise estimate would not solve that identification problem.

ECONOMIST: Correct. Precision tells us about sampling uncertainty, not which explanation is right. We must investigate competing changes at the boundary. At 21, the alcohol interpretation gains support from the legal rule and the pattern across death causes. But a jump on its own is not proof. The evidence must support the assumption that other relevant influences remain smooth.

HOST: The accepted mind map also asks us to check sorting and manipulation. People cannot choose to age themselves across a birthday. But an admissions score might be adjusted. What would make that a serious threat?

ECONOMIST: Suppose, hypothetically, unusually connected applicants could arrange a score just above the cutoff. Then applicants on opposite sides might differ in family resources or motivation. Their untreated outcomes might not join smoothly. Researchers inspect the score distribution and background characteristics for warning signs. A smooth pattern helps, but cannot prove that every unmeasured influence is balanced.

HOST: That hypothetical is useful because it explains the danger without accusing the Boston applicants of manipulation. The actual question is whether the process makes close neighbors credible comparisons. Neither an eligibility rule nor a clean graph settles that by itself.

ECONOMIST: Exactly. Another misconception is that a placebo must always equal zero in the sample. Random variation makes exact zeros unusual. We assess magnitude, uncertainty, and the pattern across checks. The internal mortality exception deserves disclosure. It also reminds us to avoid turning a collection of diagnostic tests into a mechanical pass button.

HOST: What takeaways should a student keep when facing a new cutoff study? I would start by naming the rule, running variable, treatment, and outcome. Then I would ask what would happen near the boundary without that treatment change.

ECONOMIST: Good. Examine the data before selecting the regression. Estimate the gap at the boundary, while allowing a credible smooth trend. Vary the bandwidth and reasonable trend choices. Inspect background characteristics, manipulation concerns, and placebo outcomes where appropriate. Report uncertainty. Finally, state the population and policy comparison the local result can actually inform.

HOST: For fuzzy RD, I would add an extra question: how much does treatment change when eligibility changes? Without that first stage, an outcome jump cannot be translated into a treatment effect. And even with it, I must defend the exclusion restriction.

ECONOMIST: Yes. For a binary treatment, say who the compliers are and why monotonicity is plausible. For an intensity measure, explain the scaling and the model supporting its interpretation. Remember Boston's competing channels. A valid eligibility effect can be informative even when a single channel interpretation remains harder to defend.

HOST: The thesis needs a condition attached. The map says a treatment rule's outcome jump reveals a causal effect near the threshold. That statement is helpful only if our untreated comparison is credible and competing causes do not jump there too.

ECONOMIST: Our qualified thesis is this: a threshold can reveal a local causal effect when the required continuity and treatment assumptions hold. In a sharp design, we estimate the effect of the treatment that actually switches. In a fuzzy design, interpreting the scaled effect requires the additional instrumental variables assumptions. A threshold creates an opportunity that careful design must earn.

HOST: Let me recap The Resolution. RD is more than adding a control. A discontinuity needs a causal explanation, diagnostic checks need judgment, and the conclusion stays local. Strong evidence can guide policy while still leaving unanswered questions.

ECONOMIST: That is the right balance. The mortality study offers evidence that restrictions on legal access can prevent harm near the studied age. The school study warns against judging a school's contribution by its students' impressive averages. Neither result gives us permission to generalize without examining the new setting.

## Wrap-up

HOST: Let us return to our goals. We can explain how a cutoff creates a comparison, distinguish sharp and fuzzy designs, and evaluate their assumptions and limits. The crucial idea is that nearby people can face different treatment because a rule changes abruptly.

ECONOMIST: And our thesis is conditional. A jump supports a local causal interpretation when the underlying outcome relationships remain continuous and the treatment assumptions are credible. For fuzzy designs, a first stage and valid instrumental variables assumptions connect the outcome jump to the treatment effect. The regression summarizes that argument; it does not replace it.

HOST: Here is a final think question. Suppose a selective school's admissions boundary creates a large enrollment jump. Later test scores rise smoothly with entrance scores, with no clear break. Can you conclude that selective schools have no educational value anywhere?

ECONOMIST: Pause the episode and think. Name the comparison group, the students represented, and the outcome measured before answering.

HOST: My answer is no. We would have evidence about the admission change near that cutoff, for those applicants and measured scores. We would need uncertainty estimates and information about their alternative schools. Other students, other outcomes, and other school comparisons could produce different answers.

ECONOMIST: Exactly. If we then divide by an enrollment jump, interpreting the result as an attendance effect adds assumptions. If we instead divide by a peer achievement jump, a pure peer effect interpretation adds a different exclusion claim. Naming the treatment is part of answering the question.

HOST: You can use the Colab notebook to reproduce the mortality comparisons and explore different bandwidths. The lecture slides provide another route through the assumptions, evidence, and interpretation. Compare the estimates, but also explain why the comparison could be credible.

ECONOMIST: Next, Chapter five, Differences-in-Differences, moves from a boundary in age or scores to a comparison of changes over time. We will ask how contrasting trends can help evaluate a policy, including banking during the Great Depression. Thank you for listening, and goodbye.
