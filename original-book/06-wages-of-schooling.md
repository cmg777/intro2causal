## Chapter 6

## The Wages of Schooling

Legend tells of a legendary econometrician whose econometric skills were the stuff of legend.

## Masters at Work

This chapter completes our exploration of paths from cause to effect with a multifaceted investigation of the causal effect of schooling on wages. Good questions are the foundation of our work, and the question of whether increased education really increases earnings is a classic. Masters have tackled the schooling question with all tools in hand, except, ironically, random assignment. The answers they've fashioned are no less interesting for being incomplete.

### 6.1 Schooling, Experience, and Earnings

British World War II veteran Bertie Gladwin dropped out of secondary school at age 14, though he still found work as a radio communication engineer in the British intelligence service. In his sixties, Bertie returned to school, completing a BA in psychology. Later, Bertie earned a BSc in microbiology, before embarking on a Master's degree in military intelligence, completed at the age of 91. Bertie has since been
considering study for a PhD. ${ }^{1}$
It's never too late to learn something new. Unlike Bertie Gladwin, however, most students complete their studies before establishing a career. College students spend years buried in books and tuition bills, while many of their high school friends who didn't go to college may have started work and gained a measure of financial independence. In return for the time-consuming toil and expense of college, college graduates hope to be rewarded with higher earnings down the road. Hopes and dreams are one thing; life follows many paths. Are the forgone earnings and tuition costs associated with a college degree worthwhile? That's a million dollar question, and our interest in it is more than personal. Taxpayers subsidize college attendance for students around the world, a policy motivated in part by the view that college is the key to economic success.

Economists call the causal effect of education on earnings the returns to schooling. This term invokes the notion that schooling is an investment in human capital, with a monetary payoff similar to that of a financial investment. Generations of masters have estimated the economic returns to schooling. Their efforts illustrate four of our tools: regression, DD, IV, and RD.
'Metrics master Jacob Mincer pioneered efforts to quantify the return to schooling using regression. ${ }^{2}$ Working with U.S. census data, Mincer ran regressions like

$$
\begin{equation*}
\ln Y_{i}=\alpha+\rho S_{i}+\beta_{1} X_{i}+\beta_{2} X_{i}^{2}+e_{i}, \tag{6.1}
\end{equation*}
$$

where $\ln Y_{i}$ is the $\log$ annual earnings of man $i, S_{i}$ is his schooling (measured as years spent studying), and $X_{i}$ is his years of work experience. Mincer defined the latter as age minus years of schooling minus 6, a calculation that counts all years since graduation as years of work. Masters call $X_{i}$ calculated in this way potential experience. It's customary to control for a quadratic function of potential experience to allow for the fact that, although earnings increase with experience, they
do so at a decreasing rate, eventually flattening out in middle age.
Mincer's estimates of equation (6.1) for a sample of about 31,000 nonfarm white men in the 1960 Census look like

$$
\begin{align*}
& \ln Y_{i}=\alpha+\underset{(.002)}{.070} S_{i}+e_{i} \\
& \ln Y_{i}=\alpha+\underset{(.001)}{.107} S_{i}+\underset{(.001)}{.081} X_{i}-\underset{(.00002)}{.0012} X_{i}^{2}+e_{i} . \tag{6.2}
\end{align*}
$$

With no controls, $\rho=.07$. This estimate comes from a model built with logs, so $\rho=.07$ implies average earnings rise by about $7 \%$ with each additional year of schooling (the appendix to Chapter 2 discusses regression models with logs on the left-hand side). With potential experience included as a control variable, the estimated returns increase to about .11 .

The model with potential experience controls for the fact that those with more schooling typically have fewer years of work experience, since educated men usually start full-time work later (that is, after their schooling is completed). Because $S_{i}$ and $X_{i}$ are negatively correlated, the OVB formula tells us that omitting experience, which has a positive effect on earnings, leads to a lower estimate of the returns to schooling than we can expect in long regressions that include experience controls. Mincer's estimates imply that white men with a given level of experience enjoy an $11 \%$ earnings advantage for each additional year of education. It remains to be seen, however, whether this is a causal effect. ${ }^{3}$

## Of Singers, Fencers, and PhDs: Ability Bias

Equation (6.1) compares men with more and fewer years of schooling, while holding their years of work experience fixed. Is control for potential experience sufficient for ceteris to be paribus? In other words, at a given experience level, are more- and less-educated workers equally able and diligent? Do they have the same family connections that might offer a leg up in the labor market? Such claims seem hard to swallow. Like other masters, we're pretty highly educated ourselves. And we're
smarter, harder working, and better bred than most of those who didn't stick it out in the schooling department, or so we tell ourselves. The good qualities that we imagine we share with other highly educated workers are also associated with higher earnings, complicating the causal interpretation of regression estimates like those in equation (6.2).

We can hope to improve on these simple regression estimates by controlling for attributes correlated with schooling, variables we'll call $A_{i}$ (short for "ability"). Ignoring the experience term for now and focusing on other sources of OVB, the resulting long regression can be written as

$$
\begin{equation*}
\ln Y_{i}=\alpha^{l}+\rho^{l} S_{i}+\gamma A_{i}+e_{i} \tag{6.3}
\end{equation*}
$$

The OVB formula tells us that the short regression slope from a model with no controls, $\rho^{s}$, is related to the long regression slope in model (6.3) by the formula

$$
\rho^{s}=\rho^{l}+\underbrace{\delta_{A S} \gamma}_{\text {ability bias }},
$$

where $\delta_{A S}$ is the slope from a bivariate regression of $A_{i}$ on $S_{i}$. As always, short ( $\rho^{s}$ ) equals long ( $\rho^{l}$ ) plus the regression of omitted (from short) on included ( $\delta_{A S}$ ) times the effect of omitted in long ( $\gamma$ ). In this context, the difference between short and long is called ability bias since the omitted variable is ability.

Which way does ability bias go? We've defined $A_{i}$ so that $\gamma$ in the long regression is positive (otherwise, we'd call $A_{i}$ dis-ability). Surely $\delta_{A S}$ is positive as well, implying upward ability bias: we expect the short regression $\rho^{s}$ to exceed the more controlled $\rho^{l}$. After all, our London School of Economics and MIT students tend to be high ability, at least in the sense of having high test scores and good grades in high school. On the other hand, some people cut their schooling short so as to pursue more immediately lucrative activities. Sir Mick Jagger abandoned his pursuit of a degree at the London School of Economics in 1963 to play with an outfit known as the Rolling Stones. Jagger got no satisfaction,
and he certainly never graduated from college, but he earned plenty as a singer in a rock and roll band. No less impressive, Swedish épée fencer Johan Harmenberg left MIT after 2 years of study in 1979, winning a gold medal at the 1980 Moscow Olympics, instead of earning an MIT diploma. Harmenberg went on to become a biotech executive and successful researcher. These examples illustrate how people with high ability-musical, athletic, entrepreneurial, or otherwise-may be economically successful without the benefit of an education. This suggests that $\delta_{A S}$, and hence ability bias, can be negative as easily as positive.

## The Measure of Men: Controlling Ability

Here's an easy work-around for the ability bias roadblock: collect information on $A_{i}$ and use it as a control in regressions like equation (6.3). In an effort to tackle OVB in estimates of the returns to schooling, 'metrics master Zvi Griliches used IQ as an ability control. ${ }^{4}$ Without IQ in the model, Griliches' estimate of $\rho^{s}$ in a model controlling for potential experience is .068 . Griliches' estimated short regression schooling coefficient is well below Mincer's estimate of about $11 \%$, probably due to differences in samples and dependent variables (Griliches looked at effects on hourly wages instead of annual earnings). Importantly, the addition of an IQ control knocks Griliches' estimate down to $\rho^{l}$
$=.059$, a consequence of the facts that IQ and schooling are strongly positively correlated and that higher IQ people earn more (so the effect of omitted ability in long is indeed positive).

Although intriguing, it's hard to see Griliches' findings as conclusive. IQ doesn't capture Mick Jagger's charisma or Johan Harmenberg's perseverance, dimensions of ability that are rarely measured in statistical samples. The relevant notion of ability here is an individual's earnings potential, a concept reminiscent of the potential outcomes we use to describe causal effects throughout the book. The problem with potential
outcomes, as always, is that we can never see them all, we see only the one associated with the road taken. For example, we see only the "highly educated" potential outcome in a sample of college graduates. We can't know how such people would have fared if they'd followed Johan and Mick out of college. Attempts to summarize potential earnings with a single test score are probably inadequate. Moreover, for reasons explained in Section 6.2 and detailed further in the appendix to this chapter, when schooling is mismeasured (as we think it often is), estimates with ability controls can be misleadingly small.

## Beware Bad Control

Perhaps more controls are the answer. Why not control for occupation, for example? Many data sets that report earnings also classify workers' jobs, such as manager or laborer. Surely occupation is a strong predictor of both schooling and earnings, possibly capturing traits that distinguish Mick and Johan from more average Joes. By the logic of OVB, therefore, we should control for occupation, a matter easily accomplished by including dummy variables to indicate the types of jobs held.

Although occupation is strongly correlated with both schooling and wages, occupation dummies are bad controls in regressions meant to capture causal effects of schooling on wages. The fact that Master Joshway works today as a professor and not as a nurse's aide (as he once did) is in part a reward for his extravagant schooling. It's a mistake to eliminate this benefit from our calculation by comparing only professors or nurse's aides when attempting to quantify the economic value of schooling. Even in a world where all professors earn a uniform $\$ 1$ million a year (may it soon come to pass) and all nurse's aides earn a uniform $\$ 10,000$, an experiment that randomly assigns schooling would show that schooling raises wages. The channel by which wages are increased in this notional experiment is the shift from lowly nurse's aide to elevated professorness.

There's a second, more subtle, confounding force here: bad controls create selection bias. To illustrate, suppose we're interested in the effects
of a college degree and that college completion is randomly assigned. People can work in one of two occupations, white collar and blue collar, and a college degree naturally makes white collar work more likely. Because college changes occupation for some, comparisons of wages by college degree status conditional on occupation are no longer well balanced, even when college degrees are randomly assigned and unconditional comparisons are apples-to-apples.

This troubling phenomenon is a composition effect. By virtue of random assignment, those who do and don't have a college degree are similar in every way, at least on average. Most importantly, they have the same average $Y_{0 i}$, that is, the same average earnings potential. Suppose, however, that we limit the comparison to those who have white collar jobs. The noncollege control group in this case consists entirely of especially bright workers who manage to land a white collar job without the benefit of a college education. But the white collar group that graduates from college includes these always-white-collar guys plus a weaker group that lands a white collar job by virtue of completing college but not otherwise.

We can see the consequences of this compositional difference by imagining three equal-sized groups of workers. The first group works a blue collar job with or without college (Always Blue, or AB). A second group works a white collar job irrespective of their education (Always White, or AW). Members of a third group, Blue White (BW), get a white collar job only with a college degree. These potential occupations are described in the first two columns of Table 6.1, which lists jobs obtained by those in each group in scenarios with and without a college degree.

In spite of the fact that college is randomly assigned, and simple comparisons of college and noncollege workers reveal causal effects, within-occupation comparisons are misleading. Suppose, for the sake of argument, the value of college is the same $\$ 500$ per week for all three groups. Although the three types of workers enjoy the same gains from a college education, their potential earnings (that is, their $Y_{0 i}$ values) are likely to differ. To be concrete, suppose the AW group earns $\$ 3,000$ per
week without a college degree, the AB group earns only $\$ 1,000$ per week without a college degree, and the BWs earn something in the middle, say, $\$ 2,000$ per week without a college degree. Columns (3) and (4) of Table 6.1 summarize these facts.

TABLE 6.1
How bad control creates selection bias
| Type of worker | Potential occupation |  | Potential earnings |  | Average earnings by occupation |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
|  | Without college (1) | With college (2) | Without college (3) | With college (4) | Without college (5) | With college (6) |
| Always Blue (AB) | Blue | Blue | 1,000 | 1,500 | Blue 1,500 | Blue 1,500 |
| Blue White (BW) | Blue | White | 2,000 | 2,500 |  | White 3,000 |
| Always White (AW) | White | White | 3,000 | 3,500 | White 3,000 |  |


Limiting the college/noncollege comparison to those who have white collar jobs, the average earnings of college graduates is given by the average of the $\$ 3,500$ earned by the AWs with a college degree and the $\$ 2,500$ earned by the BWs, while the average for noncollege graduates is the constant $\$ 3,000$ earned by the AWs without a college degree. Because the average of $\$ 3,500$ and $\$ 2,500$ also equals $\$ 3,000$, the conditional-on-white-collar comparison by college graduation status is zero, a misleading estimate of the returns to college, which is $\$ 500$ for everyone. The comparison of earnings by graduation status among blue collar workers is an equally misleading zero. Although random assignment of college ensures equal proportions of apples and oranges (types or groups) in the college and noncollege barrels, conditioning on white collar employment, an outcome determined in part by college graduation, distorts this balance.

The moral of the bad control story is that timing matters. Variables measured before the treatment variable was determined are generally
good controls, because they can't be changed by the treatment. By contrast, control variables that are measured later may have been determined in part by the treatment, in which case they aren't controls at all, they are outcomes. Occupation in a regression model for the causal effect of schooling is a case in point. Ability controls (such as test scores) may also have this problem, especially if test scores come from tests taken by those who have completed most of their schooling. (Schooling probably boosts test scores.) This is one more reason to question empirical strategies that rely on test scores to remove ability bias from econometric estimates of the returns to schooling. ${ }^{5}$

### 6.2 Twins Double the Fun

Twinsburg, Ohio, near Cleveland, was founded as Millsville in the early nineteenth century. Prosperous Millsville businessmen Moses and Aaron Wilcox were identical twins whom few could distinguish. Moses and Aaron were generous to Millsville in their success, a fact recognized when Millsville was renamed Twinsburg in the early nineteenth century. Since 1976, Twinsburg has embraced its zygotic heritage in the form of a summer festival celebrating twins. Millsville's annual Twins Days attract not only twins reveling in their similarities but also researchers looking for well-controlled comparisons.

Twin siblings indeed have much in common: most grow up in the same family at the same time, while identical twins even share genes. Twins might therefore be said to have the same ability as well. Perhaps the fact that one twin gets more schooling than his or her twin sibling is due mostly to the sort of serendipitous forces discussed in Chapter 2. The notion that one twin provides a good control for the other motivates a pair of studies by masters Orley Ashenfelter, Alan Krueger, and Cecilia Rouse. ${ }^{6}$ The key idea behind this work, as in many other studies using twins, is that if ability is common to a pair of twin siblings, we can remove it from the equation by subtracting one twin's data from the other's and working only with the differences between them.

The long regression that motivates a twins analysis of the returns to schooling can be written as

$$
\begin{equation*}
\ln Y_{i f}=\alpha^{l}+\rho^{l} S_{i f}+\lambda A_{i f}+e_{i f}^{l} \tag{6.4}
\end{equation*}
$$

Here, subscript $f$ stands for family, while subscript $i=1,2$ indexes twin siblings, say, Karen and Sharon or Ronald and Donald. When Ronald and Donald have the same ability, we can simplify by writing $A_{i f}=A_{f}$. This in turn implies that we can model their earnings as

$$
\begin{aligned}
& \ln Y_{1, f}=\alpha^{l}+\rho^{l} S_{1, f}+\lambda A_{f}+e_{1, f}^{l} \\
& \ln Y_{2, f}=\alpha^{l}+\rho^{l} S_{2, f}+\lambda A_{f}+e_{2, f}^{l}
\end{aligned}
$$

Subtracting the equation for Donald from that for Ronald gives

$$
\begin{equation*}
\ln Y_{1, f}-\ln Y_{2, f}=\rho^{l}\left(S_{1, f}-S_{2, f}\right)+e_{1, f}^{l}-e_{2, f}^{l} \tag{6.5}
\end{equation*}
$$

an equation from which ability disappears. ${ }^{7}$ From this we learn that when ability is constant within twin pairs, a short regression of the difference in twins' earnings on the difference in their schooling recovers the long regression coefficient, $\rho^{l}$.

Regression estimates constructed without differencing in the twins sample generate a schooling return of about $11 \%$, remarkably similar to Mincer's. This can be seen in the first column of Table 6.2. The model that produces the estimates in column (1) includes age, age squared, a dummy for women, and a dummy for whites. White twins earn less than black twins, an unusual result in the realm of earnings comparisons by race, though the gap here is not significantly different from zero.

The differenced equation (6.5) generates a schooling return of about 6\%, a result shown in column (2) of Table 6.2. This is substantially below the short regression estimate in column (1). This decline may reflect ability bias in the short model. Yet, once again, more subtle forces may also be at work.

## Twin Reports from Twinsburg

Twins are similar in many ways, including-alas-their schooling. Of 340 twin pairs interviewed for the Twinsburg schooling studies, about half report identical educational attainment. Schooling differences, $S_{1, f}$ - $S_{2, f}$, vary much less than schooling levels, $S_{i f}$. If most twins really have the same schooling, then a fair number of the nonzero differences in reported schooling may reflect mistaken reports by at least one of them. Erroneous reports, called measurement error, tend to reduce estimates of $\rho^{l}$ in equation (6.5), a fact that may account for the decline in the estimated returns to schooling after differencing. A few people reporting their schooling incorrectly sounds unimportant, yet the consequences of such measurement error can be major.

To see why mistakes matter, imagine that twins from the same family always have the same schooling. In this scenario, the only reason $S_{1, f}- S_{2, f}$ isn't zero for everyone is because schooling is sometimes misreported. Suppose such erroneous reports are due to random forgetfulness or inattention rather than something systematic. The coefficient from a regression of earnings differences on schooling differences that are no more than random mistakes should be zero since random mistakes are unrelated to wages. In an intermediate case, where some but not all of the variation in observed schooling is due to misreporting, the coefficient in equation (6.5) is smaller than it would be if schooling were reported correctly. The bias generated by this sort of measurement error in regressors is called attenuation bias. The mathematical formula for attenuation bias is derived in the chapter appendix.

TABLE 6.2
Returns to schooling for Twinsburg twins

|  | Dependent variable |  |  |  |
| :--- | :--- | :--- | :--- | :--- |
|  | Log wage (1) | Difference in log wage (2) | Log wage (3) | Difference in log wage (4) |
| Years of education | . 110 (.010) |  | . 116 (.011) |  |
| Difference in years of education |  | . 062 (.020) |  | . 108 (.034) |
| Age | . 104 (.012) |  | . 104 (.012) |  |
| Age squared/100 | -. 106 (.015) |  | -. 106 (.015) |  |
| Dummy for female | -. 318 (.040) |  | -. 316 (.040) |  |
| Dummy for white | -. 100 (.068) |  | -. 098 (.068) |  |
| Instrument education with twin report | No | No | Yes | Yes |
| Sample size | 680 | 340 | 680 | 340 |

Notes: This table reports estimates of the returns to schooling for Twinsburg twins. Column (1) shows OLS estimates from models estimated in levels. OLS estimates of models for cross-twin differences appear in column (2). Column (3) reports 2SLS estimates of a levels regression using sibling reports as instruments for schooling. Column (4) reports 2SLS estimates using the difference in sibling reports to instrument the cross-twin difference in schooling. Standard errors appear in parentheses.

Misreported schooling attenuates the levels regression estimates shown in column (1) of Table 6.2, but less so than the differenced estimates in column (2). This difference in the extent of attenuation bias is also illustrated by the hypothetical scenario where all twins share the same schooling but schooling levels differ across families. When twins in the same family really have the same schooling, all variation in withinfamily differences in reported schooling comes from mistakes. By contrast, most of the cross-family variation in reported schooling reflects real differences in education. Real variation in schooling is related to earnings, a fact that moderates attenuation bias in estimates of the model for levels, equation (6.4). This reflects a general point about the consequences of covariates for models with mismeasured regressorsadditional controls make attenuation bias worse-a point detailed in the
chapter appendix.
Measurement error raises an important challenge for the Twinsburg analysis, since measurement error alone may explain the pattern of results seen in columns (1) and (2) of Table 6.2. Moving from the levels to the differenced regression accentuates attenuation bias, probably more than a little. The decline in schooling coefficients across columns may therefore have little to do with ability bias. Fortunately, seasoned masters Ashenfelter, Krueger, and Rouse anticipated the attenuation problem. They asked each twin to report not only their own schooling but also that of their sibling. As a result, the Twinsburg data sets contain two measures of schooling for each twin, one self-report and one sibling report. The sibling reports provide leverage to reduce, and perhaps even eliminate, attenuation bias.

The key tool in this case, as with many of the other problems we've encountered, is IV. Karen and Sharon make mistakes when reporting each other's schooling as well as when reporting their own. As long as the mistakes in Karen's report of her sister's schooling are unrelated to mistakes in her sister's self-report, and vice versa, Karen's report of Sharon's schooling can be used as an instrument for Sharon's self-report, and vice versa. IV eliminates attenuation bias in the levels regression as well as in estimates of the differenced model (though the levels regression is still more likely than the differenced regression to suffer from ability bias).

As always, an IV estimate is the ratio of reduced-form estimates to first-stage estimates. When instrumenting the levels equation, the reduced-form estimate is the effect of Karen's report of Sharon's schooling on Sharon's earnings. The corresponding first-stage estimate is the effect of Karen's report of Sharon's schooling on Sharon's selfreported schooling. Reduced-form and first-stage results are still subject to attenuation bias. But when we divide one by the other, these biases cancel out, leaving us with an unattenuated IV estimate.

IV works similarly in the first differenced model. The instrument for within-family differences in schooling is the difference in the crosssibling reports. Provided that measurement errors in own- and cross-
sibling schooling reports are uncorrelated, IV produces the no-OVB, unattenuated long-regression return to schooling, $\rho^{l}$, that we set out to obtain. Uncorrelatedness of reporting errors across siblings is a strong assumption, but a natural starting point for any exploration of bias from measurement error.

IV estimates of the levels equation appear in column (3) of Table 6.2 (as always, we execute this IV procedure by running 2SLS, which works no less well with instruments that are not dummy variables). Instrumenting self-reported schooling with cross-sibling reported schooling increases the estimated return to schooling only a little, from .110 to .116 . This result is consistent with the notion that there's little measurement error in the level of schooling. By contrast, instrumenting the differenced equation boosts the estimated return to schooling from .062 to .108. This result, reported in column (4) of Table 6.2, points to considerable measurement error in the differenced data. At the same time, the differenced IV estimate of .108 is not far below the crosssectional estimate of .116, suggesting the problem we set out to solveability bias in estimates of the returns to schooling-isn't such a big deal after all.

### 6.3 Econometricians Are Known by Their ... Instruments

## It's the Law

Economists think people make important choices such as those related to schooling by comparing anticipated costs with expected benefits. The cost of staying in secondary school is determined partly by compulsory schooling laws, which punish those who leave school too soon. Since you avoid punishment by staying in school, compulsory schooling laws make extra schooling seem cheaper relative to the alternative, dropping out. This generates a causal chain reaction leading from compulsory schooling laws to schooling choices to earnings that might reveal the economic returns to schooling. The 'metrics methods behind this idea are those of Chapters 3 and 5: instrumental variables and differences-
indifferences.
As always, IV begins with the first stage. One hundred years ago, there were few compulsory attendance laws, while today most American states keep students in school until at least age 16. Many states also forbid school-aged children from working, or require school authorities to give permission for a child to work. Assuming that some students would otherwise drop out if not for such laws, stricter compulsory school requirements should increase average schooling. Provided changes in state compulsory attendance laws are also unrelated to the potential earnings of residents in each state (as determined by things like family background, the states' industrial structure, or other policy changes), these laws create valid instruments for schooling in equations like (6.1).

But compulsory attendance laws probably are related to potential earnings. In the early twentieth century, for example, agricultural Southern states had few compulsory attendance requirements, while compulsory schooling laws were stricter in the more industrial North. Simple comparisons of earnings across U.S. regions typically reveal vast differences in earnings, but these are mostly unrelated to the North's more rigorous schooling requirements. Compulsory schooling requirements also grew stricter over time, but here, too, simple comparisons are misleading. Many features of the American economy changed as the twentieth century progressed; compulsory schooling laws are but a small part of this ever-evolving economic story.

A creative combination of DD and IV offers a possible way around OVB roadblocks in this context. Compulsory schooling requirements expanded and tightened most dramatically in the first half of the twentieth century. Masters Joshway and Daron Acemoglu collected state-by-year information on the compulsory schooling laws applicable to those who might have been in school at this time. ${ }^{8}$ These laws include child labor provisions as well as compulsory attendance requirements. Child labor laws that require a certain amount of schooling be completed before children are allowed to work seem to have increased schooling more than attendance requirements. A useful simplification in this context uses the laws in effect in census respondents' states of birth at
the time they were 14 years old to identify states and years in which 7 , 8 , and 9 or more years of schooling were required before work was allowed. The resulting set of instrumental variables consists of dummies for each of these three categories; the omitted category consists of states and years in which 6 or fewer years of schooling were required before work was allowed.

Because child labor instruments vary with both state and year of birth, they can be used to estimate a first-stage equation that controls for possible time effects through the inclusion of year-of-birth dummies, while controlling for state characteristics through the inclusion of state-of-birth dummies. Control for state effects should mitigate bias from regional differences that are correlated with compulsory schooling provisions, while the inclusion of year-of-birth effects should mitigate bias from the fact that earnings differ across birth cohorts for many reasons besides compulsory schooling laws. The resulting first-stage equation looks like the Chapter 5 regression DD model (described by equation (5.5)) used to estimate the effect of state and year changes in the MLDA on death rates. Here, however, year-of-birth dummies replace dummies for calendar time.

The Acemoglu and Angrist compulsory schooling first-stage equation was estimated with an extract of men in their forties, drawn from each of the U.S. census samples available every decade from 1950 to 1990. Stacking these five censuses produces a single large data set in which different censuses contribute different cohorts. For example, men in their forties observed in the 1950 Census were born from 1900 to 1909 and subject to laws in effect in the 1910s and 1920s, while men in their forties observed in the 1960 Census were born from 1910 to 1919 and subject to laws in effect in the 1920s and 1930s.

The first-stage estimates reported in column (1) of Table 6.3 suggest that child labor laws requiring 7 or 8 years of schooling before work was allowed increased schooling (measured as highest grade completed) by about two-tenths of a year. Laws requiring 9 or more years of schooling before work was allowed had an effect twice as large. A parallel set of reduced-form estimates appear in column (3) of the table. These come
from regression models similar to those used to construct the first-stage estimates reported in column (1), with the log weekly wage replacing years of schooling as the dependent variable. Laws requiring 7 or 8 years of schooling before work was allowed appear to have raised wages by about $1 \%$, while laws requiring 9 or more years of schooling before work increased earnings by almost $5 \%$, though only the latter estimate is significant. The 2SLS estimate generated by these estimates is .124 (with an estimated standard error of .036).

A $12 \%$ wage gain for each additional year of schooling is impressive, all the more so since the schooling increase in question is involuntary. Stronger compulsory schooling laws appear to raise schooling, and this in turn produces higher wages for the men constrained by these laws (compulsory schooling compliers, in this case). Especially interesting is the fact that the 2SLS estimate of the returns to schooling generated by compulsory schooling instruments exceeds the corresponding OLS estimate of .075 . This finding weighs against the notion of upward ability bias in the OLS estimate.

TABLE 6.3
Returns to schooling using child labor law instruments
|  | Dependent variable |  |  |  |
| :--- | :--- | :--- | :--- | :--- |
|  | Years of schooling |  | Log weekly wages |  |
|  | (1) | (2) | (3) | (4) |
| A. First-stage and reduced-form estimates |  |  |  |  |
| Child labor law req. 7 years | . 166 (.067) | -. 024 (.048) | . 010 (.011) | -. 013 (.011) |
| Child labor law req. 8 years | . 191 (.062) | . 024 (.051) | . 013 (.010) | . 005 (.010) |
| B. Second-stage estimates |  |  |  |  |
| Years of education |  |  | . 124 (.036) | . 399 (.360) |
| State of birth dummies × linear year of birth trends | No | Yes | No | Yes |


#### Abstract

Notes: This table shows 2SLS estimates of the returns to schooling using as instruments three dummies indicating the years of schooling required by child labor laws as a condition for employment. Panel A reports first-stage and reduced-form estimates controlling for year and state of birth effects and for census year dummies. Columns (2) and (4) show the results of adding state-specific linear trends to the list of controls. Panel B shows the 2SLS estimates of the returns to schooling generated by the first-stage and reduced-form estimates in panel A. Sample size is 722,343. Standard errors are reported in parentheses.


Before declaring mission accomplished, a master looks for threats to validity. The variation in schooling generated by compulsory schooling laws produces a DD-style first stage and reduced form. As discussed in Chapter 5, the principal threat to validity in this context is omitted statespecific trends. Specifically, we must worry that states in which compulsory schooling laws grew stricter simultaneously experienced unusually large wage growth across cohorts for reasons unrelated to schooling. Perhaps wage growth and changes in schooling laws are both driven by some third variable, say, changes in industrial structure.

The case for omitted variables bias in this context grows even stronger once we recognize that most of the action in the compulsory schooling research design comes from comparisons of Northern and Southern states. Southern states saw enormous economic growth in the twentieth century, while at the same time, social legislation in these states proliferated. The relative growth in earnings in Southern states might have been caused in part by more restrictive compulsory attendance provisions. But it might not.

Chapter 5 explains that a simple check for state-specific trends adds a linear time trend for each state to the model of interest. In this case, the relevant time dimension is year of birth, so the model with state-specific trends includes a separate linear year-of-birth variable for each state of birth in the sample (the regression model with year-of-birth trends looks like equation (5.6)).

Columns (2) and (4) in Table 6.3 report the results of this addition. The estimates in these columns offer little evidence that compulsory schooling laws matter for either schooling or wages. First-stage and reduced-form estimates both fall precipitously in the model with trends, and none are significantly different from zero. Importantly, the first-
stage estimates in column (2) are more precise (that is, have smaller standard errors) than those estimated without state-specific trends. Lack of statistical significance therefore comes from the fact that the estimates with trends are much smaller and not from reduced precision. The reduced-form estimates in column (4) similarly offer little evidence of a link between compulsory school laws and earnings. The 2SLS estimate generated by columns (2) and (4) comes out at an implausibly large .399, but with a standard error almost as large. Sad to say for Master Joshway, Table 6.3 reveals a failed research design.

## To Everything There Is a Season (of Birth)

master oogway: Yesterday is history, tomorrow is a mystery, but today is a gift. That is why it is called the present.

Kung Fu Panda

You get presents on your birthday, but some birth dates are better than others. A birthday that falls near Christmas might reduce your windfall if gift givers try to make one present do double duty. On the other hand, many Americans born late in the year get surprise gifts in the form of higher schooling and higher earnings.

The path leading from late-year births to increased schooling and earnings starts in kindergarten. In most states, children enter kindergarten in the year they turn 5, whether or not they've had a fifth birthday by the time school starts in early September. Jae, born on January 1st, was well on the way toward his sixth birthday when he started school. By contrast, Dante, born on December 1st, was not even 5 when he started. Such birthday-based differences in school-starting age are life changing for some.

The life-changing nature of school-starting age is an unintended consequence of American compulsory attendance laws. By the middle of the twentieth century, most states were allowing students to leave school (that is, to drop out of high school) only after they'd turned 16 (some states require attendance until 17 or 18). Most compulsory attendance
laws allow you to quit school once you've reached the dropout age, without finishing the school year. Jae, having started school at the ripe old age of 5 years and 8 months, turned 16 in January ten years later, early in his tenth-grade year. Dante, having started school at the tender age of 4 years and 9 months, turned 16 in December eleven years later, after finishing tenth grade and starting eleventh. Both were itching to leave school as soon as they were allowed, and each dropped out immediately on turning 16. But Dante, having started school younger, was forced by accident of birth to complete one more grade than Jae.

You can't pick your birthday. Even your parents probably found your birthday hard to fix. Ultimately, birth timing has a good deal of randomness to it, mimicking experimental random assignment. By virtue of the partly random nature of birth dates, men like Jae and Dante, born at different times of the year, are likely to have similar family backgrounds and talents, even though they have very different educational attainment. This sounds like a promising scenario for IV, and it is.

Masters Joshway and Alan Krueger used differences in schooling generated by quarter of birth (QOB) to construct IV estimates of the economic returns to compulsory schooling. ${ }^{9}$ Angrist and Krueger analyzed large publicly available samples from the 1970 and 1980 U.S. Censuses, samples similar to those used by Acemoglu and Angrist. Somewhat unusually for publicly available data sets, these census files contain information on respondents' QOB.

The QOB first stage for 1980 Census respondents appears in Figure 6.1. This figure plots average schooling by year and QOB for men born in the 1930s. Most men in these cohorts finished high school, so their average highest grade completed ranges from 12 to 13 years. Figure 6.1 exhibits a surprising sawtooth pattern: Men born earlier in the year tend to have lower average schooling than those born later. The teeth of the saw have an amplitude of about .15. This may not seem like much, but it's consistent with the story of Jae and Dante. Among men born in the 1930s, about $20 \%$ left school in grade 10 or sooner. Late-quarter births impose about .75 of a grade's worth of extra schooling on this $20 \%$. The
calculation $.2 \times .75=.15$ accounts for the ups and downs in Figure 6.1.

As always, IV is the ratio of the reduced form to the corresponding first stage. The QOB reduced form is plotted in Figure 6.2. The flatness of earnings from year to year seen in this figure isn't surprising. Earnings initially increase sharply with age, but the age-earnings profile tends to flatten out for men in their forties. Importantly, however, the QOB sawtooth in schooling is paralleled by a similar QOB sawtooth in average earnings. Men born later in the year not only get more schooling than those born earlier, they have higher earnings as well. IV logic attributes the sawtooth pattern in average earnings by QOB to the sawtooth pattern in average schooling by QOB.

FIGURE 6.1
The quarter of birth first stage
![](https://cdn.mathpix.com/cropped/4440deb8-2d2c-4497-bc23-c426fcbef9da-246.jpg?height=525&width=1032&top_left_y=1287&top_left_x=532)

[^12]figure 6.2
The quarter of birth reduced form

![](https://cdn.mathpix.com/cropped/4440deb8-2d2c-4497-bc23-c426fcbef9da-247.jpg?height=523&width=1024&top_left_y=262&top_left_x=545)
Notes: This figure plots average log weekly wages by quarter of birth for men born in 19301939 in the 1980 U.S. Census. Quarters are labeled 1-4, and symbols for the fourth quarter are filled in.

A simple QOB-based IV estimate compares the schooling and earnings of men born in the fourth quarter to the schooling and earnings of men born in earlier quarters. Table 6.4 organizes the ingredients for this IV recipe using the same sample as was used to construct Figure 6.1. Men born in the fourth quarter earn a little more than those born earlier, a difference of about $.7 \%$. Fourth-quarter births also have higher average educational attainment; here, the difference is about .09 years. Dividing the first difference by the second, we have

Effect of schooling on wages

$$
\begin{aligned}
& =\frac{\{\text { Effect of } Q O B \text { on wages }\}}{\{\text { Effect of } Q O B \text { on schooling }\}} \\
& =\frac{.0068}{.0092}=.074
\end{aligned}
$$

## TABLE 6.4

IV recipe for an estimate of the returns to schooling using a single quarter of birth instrument

|  | Born in quarters 1-3 | Born in quarter 4 | Difference |
| :--- | :--- | :--- | :--- |
| Log weekly wage | 5.8983 | 5.9051 | . 0068 (.0027) |
| Years of education | 12.7473 | 12.8394 | . 0921 (.0132) |
| IV estimate of the returns to schooling |  |  | . 074 (.028) |

Notes: Sample size is 329,509 . Standard errors are reported in parentheses.

TABLE 6.5
Returns to schooling using alternative quarter of birth instruments
|  | OLS (1) | 2SLS (2) | OLS (3) | 2SLS (4) | 2SLS (5) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Years of education | . 071 (.0004) | . 074 (.028) | . 071 (.0004) | . 075 (.028) | . 105 (.020) |
| First-stage $F$-statistic |  | 48 |  | 47 | 33 |
| Instruments | None | Quarter 4 | None | Quarter 4 | 3 quarter dummies |
| Year of birth controls | No | No | Yes | Yes | Yes |


Notes: This table reports OLS and 2SLS estimates of the returns to schooling using quarter of birth instruments. The estimates in columns (3)-(5) are from models controlling for year of birth. Columns (1) and (3) show OLS estimates. Columns (2), (4), and (5) show 2SLS estimates using the instruments indicated in the third row of the table. F-tests for the joint significance of the instruments in the corresponding first-stage regression are reported in the second row. Sample size is 329,509 . Standard errors are reported in parentheses.

By way of comparison, the bivariate regression of log weekly wages on schooling comes out remarkably close, at .071. These simple OLS and IV estimates are repeated in the first two columns of Table 6.5. The columns containing IV estimates are labeled "2SLS" because, as always, that's how we do IV.

As with the IV estimates of the effects of family size discussed in Chapter 3, we can use 2SLS to add covariates and additional instruments to the QOB IV story. OLS and 2SLS estimates of models including year of
birth dummies (a control for age in our 1980 cross section) appear in columns (3) and (4) of Table 6.5. These results are almost indistinguishable from those in columns (1) and (2). Adding dummies for first and second quarters of birth to the instrument list, however, leads to a noteworthy gain in precision. The three-instrument estimate, reported in column (5), is larger than single-instrument estimates reported in columns (2) and (4), with a standard error that falls from .028 to . 020 .

What's required for 2SLS estimates using QOB instruments to capture the causal effect of education on earnings? First, the instruments must predict the regressor of interest (in this case, schooling). Second, the instruments should be as good as randomly assigned in the sense of being independent of omitted variables (in this case, variables like family background and ability). Finally, QOB should affect outcomes solely through the channel we've chosen as the variable to be instrumented (in this case, schooling). Other channels must be excluded. It's worth asking how QOB instruments measure up to these first-stage, independence, and exclusion restriction requirements.

We've seen that QOB produces a clear sawtooth pattern in highest grade completed. This is a compelling visual representation of a strong first stage, confirmed by the large $F$-statistics in Table 6.5. As discussed in the appendix to Chapter 3, a large first-stage $F$-statistic suggests bias from weak instruments is unlikely to be a problem in this context.

Is QOB independent of maternal characteristics? Birthdays aren't literally randomly assigned, of course. Researchers have long documented season of birth patterns in mothers' socioeconomic background. A recent study by Kasey Buckles and Daniel Hungerman explores these patterns further. ${ }^{10}$ Buckles and Hungerman find that maternal schooling-a good measure of family background-peaks for mothers who give birth in the second quarter. This suggests that family background cannot account for the seasonal pattern in schooling and wages seen in Figures 6.1 and 6.2, both of which exhibit third- and fourth-quarter peaks. In fact, average maternal schooling by QOB is slightly negatively correlated with average offspring schooling by QOB.

Not surprisingly, therefore, control for average maternal characteristics moderately increases IV estimates of schooling returns using QOB instruments. Season of birth variation in family background, though not zero, does not follow a pattern that changes QOB-based 2SLS estimates substantially.

Finally, what of exclusion? The QOB first stage is generated by the fact that later-born students enter school younger than those born earlier in the year, and therefore complete more schooling before they're allowed to drop out. But what if school-starting age itself matters? The most commonly told entry-age story is that the youngest children in a firstgrade class are at a disadvantage, while children who are a little older than their classmates tend to do better. Here too, the circumstantial evidence for QOB instruments is encouraging. The crux of the QOBcompulsory schooling story is that younger entrants ultimately come out ahead, and this is what the data show. ${ }^{11}$

Empirical strategies are never perfect. Weak nails bend, but the house of 'metrics needn't collapse. We can't prove that a particular IV strategy satisfies the assumptions required for a causal interpretation. The econometrician's position is necessarily defensive. As we've seen, however, key assumptions can be probed and checked in a variety of ways, and so they must be. Masters routinely check their own work and assumptions, while carefully evaluating results reported by others.

On the substantive side, IV estimates using QOB instruments come out similar to or larger than the corresponding OLS estimates of the economic return to schooling. Modest measurement error in the schooling variable might explain the gap between 2SLS and OLS estimates, much as in the twins data. These results suggest downward bias from mismeasured schooling matters as much or more than any ability bias that causes us to overestimate the economic value of education. The earnings gain generated by an additional grade completed seems to be about $7-10 \%$. Bertie Gladwin might have accomplished even more had he finished his schooling sooner.

### 6.4 Rustling Sheepskin in the Lone Star State

Schooling means many things, and every educational experience is different. But economists look at diverse educational experiences and see them all as creating human capital: a costly investment in skills from which we also expect to see a return. Some students, like Bertie Gladwin, enjoy school for its own sake and show little interest in economic returns. But many more probably see their schooling as stressful, tiring, and expensive. In addition to tuition costs, time spent in school could have been spent working. Many college students spend relatively little on tuition, but all full-time students pay an opportunity cost. This notion -that a large part of the costs of acquiring an education comes in the form of forgone earnings-leads us to expect each year of additional schooling to generate about the same economic return, whether it's the tenth, twelfth, or twentieth year at the books. The simple human capital view of schooling embodies this idea.

Of course, people who have not had the benefit of economics training probably don't think about education like this. Most measure their educational attainment in terms of degrees instead of years. Few job applicants describe themselves as having completed " 17 years of schooling." Rather, applicants list the schools from which they graduated and the dates of degrees received. To an economist, however, degrees are just pieces of paper that should have little or no real value. Master Stevefu is a case in point: though he spent many years in college, attending Susquehanna University in central Pennsylvania (among other fine institutions) he has yet to earn his bachelor's degree. Reflecting this dismissive view of the value of certification, economists refer to the hypothesis that degrees matter as "sheepskin effects," after the material on which diplomas were originally inscribed.

The search for sheepskin effects led Masters Damon Clark and Paco Martorell to a clever fuzzy RD research design. ${ }^{12}$ They exploit the fact that in Texas, as in many other states, receipt of a high school diploma is conditional on satisfactory completion of an exit exam in addition to state-required coursework. Students first take this exam in tenth or
eleventh grade, with retests scheduled periodically for those who fail. A last-chance exit exam for those who have failed previously is administered at the end of twelfth grade. In truth this isn't the last chance for a Texas senior to earn a diploma; it's possible to try again later. Still, for many who take it, the last-chance exam is decisive.

The decisive nature of the last-chance exit exam for many Texas high school seniors is documented in Figure 6.3, which plots the probability of diploma receipt against last-chance exam scores, centered at the passing threshold. The figure, which plots averages conditional on each score value along with fitted values from a fourth-order polynomial estimated separately on either side of the passing cutoff, shows diploma award rates close to .5 for students who miss the cutoff. For those whose scores clear the cutoff, however, diploma award rates jump above $90 \%$. This change is discontinuous and unambiguous: Figure 6.3 documents a fuzzy RD first stage of nearly .5 for the effects of exit exam passage on diploma receipt.

Many of those who earn a diploma go on to college, in which case their earnings stay low until this additional schooling is also completed. It's therefore important to look far enough down the road for any sheepskin effect in earnings to emerge. Clark and Martorell used data from the Texas unemployment insurance system, which records longitudinal information on the earnings of most workers in the state, to follow the earnings of those taking the last-chance exam for up to 11 years.

Earnings data for a period ranging from 7-11 years after students sat for their last-chance exit exam show no evidence of sheepskin effects. This can be seen in Figure 6.4, which plots average annual earnings against exam scores in a format paralleling that of Figure 6.3 (earnings here are in dollars and not in logs, and the averages include zeros for people who aren't working). Figure 6.4 is a picture of the reduced form in a fuzzy RD design that uses a dummy for passing the exit exam as an instrumental variable for the effect of diploma receipt on earnings. As always, when the reduced form is zero-in this case, no jump appears in Figure 6.4-we know that the corresponding 2SLS estimate is zero as
well.

FIGURE 6.3
Last-chance exam scores and Texas sheepskin
![](https://cdn.mathpix.com/cropped/4440deb8-2d2c-4497-bc23-c426fcbef9da-253.jpg?height=472&width=1017&top_left_y=562&top_left_x=550)

Notes: Last-chance exam scores are normalized relative to passing thresholds. Dots show average diploma receipt conditional on each score value. The solid lines are fitted values from a fourth-order polynomial, estimated separately on either side of the passing cutoff (indicated by the vertical dashed line).

FIGURE 6.4
The effect of last-chance exam scores on earnings
![](https://cdn.mathpix.com/cropped/4440deb8-2d2c-4497-bc23-c426fcbef9da-253.jpg?height=447&width=1017&top_left_y=1506&top_left_x=545)

Notes: Last-chance exam scores are normalized relative to passing thresholds. Dots show average earnings conditional on each score value, including zeros for nonworkers. The solid lines are fitted values from a fourth-order polynomial, estimated separately on either side of the passing cutoff (indicated by the vertical dashed line).

The 2SLS estimates generated by dividing the first-stage and reducedform discontinuities seen in Figures 6.3 and 6.4 show a diploma effect of $\$ 52$ (with a standard error of about $\$ 630$ ). This amounts to less than
half a percent of average earnings, which are about $\$ 13,000$. These are small effects indeed, weighing against the sheepskin hypothesis. On the other hand, the associated confidence intervals also include earnings effects of nearly $10 \%$.

Large standard errors leave us with the possibility of some sheepskin effects, so the search for evidence on this point will surely continue. Masters know the search for econometric truth never ends, and that what is good today will be bettered tomorrow. Our students teach us this.
![](https://cdn.mathpix.com/cropped/4440deb8-2d2c-4497-bc23-c426fcbef9da-254.jpg?height=1271&width=1165&top_left_y=918&top_left_x=433)
master stevefu: Time for you to leave, Grasshopper. You must continue your journey alone. Remember, when you follow the 'metrics path, anything is possible.
take the measure of the evidence.

## Appendix: Bias from Measurement Error

You've dreamed of running the regression

$$
\begin{equation*}
Y_{i}=\alpha+\beta S_{i}^{*}+e_{i}, \tag{6.6}
\end{equation*}
$$

but data $S_{i}^{*}$, on the regressor of your dreams, are unavailable. You see only a mismeasured version, $S_{i}$. Write the relationship between observed and desired regressors as

$$
\begin{equation*}
S_{i}=S_{i}^{*}+m_{i}, \tag{6.7}
\end{equation*}
$$

where $m_{i}$ is the measurement error in $S_{i}$. To simplify, assume errors average to zero and are uncorrelated with $s_{i}^{*}$ and the residual, $e_{i}$. Then we have

$$
\begin{aligned}
E\left[m_{i}\right] & =0 \\
C\left(S_{i}^{*}, m_{i}\right) & =C\left(e_{i}, m_{i}\right)=0 .
\end{aligned}
$$

These assumptions describe classical measurement error (jazzier forms of measurement error may rock your regression coefficients even more).

The regression coefficient you're after, $\beta$ in equation (6.6), is given by

$$
\beta=\frac{C\left(Y_{i}, S_{i}^{*}\right)}{V\left(S_{i}^{*}\right)}
$$

Using the mismeasured regressor, $S_{i}$, instead of $S_{i}^{*}$, you get

$$
\begin{equation*}
\beta_{b}=\frac{C\left(Y_{i}, S_{i}\right)}{V\left(S_{i}\right)}, \tag{6.8}
\end{equation*}
$$

where $\beta_{b}$ has a subscript " $b$ " as a reminder that this coefficient is biased.
To see why $\beta_{b}$ is a biased version of the coefficient you're after, use
equations (6.6) and (6.7) to substitute for $Y_{i}$ and $S_{i}$ in the numerator of equation (6.8):

$$
\begin{aligned}
\beta_{b} & =\frac{C\left(Y_{i}, S_{i}\right)}{V\left(S_{i}\right)} \\
& =\frac{C\left(\alpha+\beta S_{i}^{*}+e_{i}, S_{i}^{*}+m_{i}\right)}{V\left(S_{i}\right)} \\
& =\frac{C\left(\alpha+\beta S_{i}^{*}+e_{i}, S_{i}^{*}\right)}{V\left(S_{i}\right)}=\beta \frac{V\left(S_{i}^{*}\right)}{V\left(S_{i}\right)} .
\end{aligned}
$$

The next-to-last equals sign here uses the assumption that measurement error, $m_{i}$, is uncorrelated with $S_{i}^{*}$ and $e_{i}$; the last equals sign uses the fact that $S_{i}^{*}$ is uncorrelated with a constant and with $e_{i}$, since the latter is a residual from a regression on $S_{i}^{*}$. We've also used the fact that the covariance of $S_{i}^{*}$ with itself is its variance (see the appendix to Chapter 2 for an explanation of these and related properties of variance and covariance).

We've assumed that $m_{i}$ is uncorrelated with $S_{i}^{*}$. Because the variance of the sum of uncorrelated variables is the sum of their variances, this implies

$$
V\left(S_{i}\right)=V\left(S_{i}^{*}\right)+V\left(m_{i}\right)
$$

which means we can write

$$
\begin{equation*}
\beta_{b}=r \beta, \tag{6.9}
\end{equation*}
$$

where

$$
r=\frac{V\left(S_{i}^{*}\right)}{V\left(S_{i}\right)}=\frac{V\left(S_{i}^{*}\right)}{V\left(S_{i}^{*}\right)+V\left(m_{i}\right)}
$$

is a number between zero and one.
The fraction $r$ describes the proportion of variation in $S_{i}$ that is
unrelated to mistakes and is called the reliability of $S_{i}$. Reliability determines the extent to which measurement error attenuates $\beta_{b}$. The attenuation bias in $\beta_{b}$ is

$$
\beta_{b}-\beta=-(1-r) \beta,
$$

so that $\beta_{b}$ is smaller than (a positive) $\beta$ unless $r=1$, and there's no measurement error after all.

## Adding Covariates

In Section 6.1, we noted that the addition of covariates to a model with mismeasured regressors tends to exacerbate attenuation bias. The Twinsburg story told in Section 6.2 is a special case of this, where the covariates are dummies for families in samples of twins. To see why covariates increase attenuation bias, suppose the regression of interest is

$$
\begin{equation*}
Y_{i}=\alpha+\beta S_{i}^{*}+\gamma X_{i}+e_{i}, \tag{6.10}
\end{equation*}
$$

where $X_{i}$ is a control variable, perhaps IQ or another test score. We know from regression anatomy that the coefficient on $S_{i}^{*}$ in this model is given by

$$
\beta=\frac{C\left(Y_{i}, \tilde{S}_{i}^{*}\right)}{V\left(\tilde{S}_{i}^{*}\right)},
$$

where $\tilde{S}_{i}^{*}$ is the residual from a regression of $S_{i}^{*}$ on $X_{i}$. Likewise, replacing $S_{i}^{*}$ with $S_{i}$, the coefficient on $S_{i}$ becomes

$$
\beta_{b}=\frac{C\left(Y_{i}, \tilde{S}_{i}\right)}{V\left(\tilde{S}_{i}\right)},
$$

where $\tilde{s}_{i}$ is the residual from a regression of $S_{i}$ on $X_{i}$.
Add the (classical) assumption that measurement error, $m_{i}$, is
uncorrelated with the covariate, $X_{i}$. Then the coefficient from a regression of mismeasured $S_{i}$ on $X_{i}$ is the same as the coefficient from a regression of $S_{i}^{*}$ on $X_{i}$ (use the properties of covariance and the definition of a regression coefficient to see this). This in turn implies that

$$
\tilde{S}_{i}=\tilde{S}_{i}^{*}+m_{i}
$$

where $m_{i}$ and $\tilde{S}_{i}^{*}$ are uncorrelated. We therefore have

$$
V\left(\tilde{S}_{i}\right)=V\left(\tilde{S}_{i}^{*}\right)+V\left(m_{i}\right)
$$

Applying the logic used to establish equation (6.9), we get

$$
\begin{align*}
\beta_{b} & =\frac{C\left(Y_{i}, \tilde{S}_{i}\right)}{V\left(\tilde{S}_{i}\right)} \\
& =\frac{V\left(\tilde{S}_{i}^{*}\right)}{V\left(\tilde{S}_{i}^{*}\right)+V\left(m_{i}\right)} \beta=\tilde{r} \beta \tag{6.11}
\end{align*}
$$

where

$$
\tilde{r}=\frac{V\left(\tilde{S}_{i}^{*}\right)}{V\left(\tilde{S}_{i}^{*}\right)+V\left(m_{i}\right)}
$$

Like $r$, this lies between zero and one.
What's new here? The variance of $\tilde{S}_{i}^{*}$ is necessarily reduced relative to that of $S_{i}^{*}$, because the variance of $\tilde{S}_{i}^{*}$ is the variance of a residual from a regression model in which $S_{i}^{*}$ is the dependent variable. Since $V\left(\tilde{S}_{i}^{*}\right)<V\left(S_{i}^{*}\right)$, we also have

$$
\tilde{r}=\frac{V\left(\tilde{S}_{i}^{*}\right)}{V\left(\tilde{S}_{i}^{*}\right)+V\left(m_{i}\right)}<\frac{V\left(S_{i}^{*}\right)}{V\left(S_{i}^{*}\right)+V\left(m_{i}\right)}=r
$$

This explains why adding covariates to a model with mismeasured schooling aggravates attenuation bias in estimates of the returns to
schooling. Intuitively, this aggravation is a consequence of the fact that covariates are correlated with accurately measured schooling while being unrelated to mistakes. The regression-anatomy operation that removes the influence of covariates therefore reduces the information content of a mismeasured regressor while leaving the noise componentthe mistakes-unchanged (test your understanding of the formal argument here by deriving equation (6.11)). This argument carries over to the differencing operation used to purge ability from equation (6.4): differencing across twins removes some of the signal in schooling, while leaving the variance of the noise unchanged.

## IV Clears Our Path

Without covariates, the IV formula for the coefficient on $S_{i}$ in a bivariate regression is

$$
\begin{equation*}
\beta_{I V}=\frac{C\left(Y_{i}, Z_{i}\right)}{C\left(S_{i}, Z_{i}\right)} \tag{6.12}
\end{equation*}
$$

where $Z_{i}$ is the instrument. In Section 6.2, for example, we used crosssibling reports to instrument for possibly mismeasured self-reported schooling. Provided the instrument is uncorrelated with the measurement error and the residual, $e_{i}$, in equations like (6.6), IV eliminates the bias due to mismeasured $S_{i}$.

To see why IV works in this context, use equations (6.6) and (6.7) to substitute for $Y_{i}$ and $S_{i}$ in equation (6.12):

$$
\begin{aligned}
\beta_{I V} & =\frac{C\left(Y_{i}, Z_{i}\right)}{C\left(S_{i}, Z_{i}\right)}=\frac{C\left(\alpha+\beta S_{i}^{*}+e_{i}, Z_{i}\right)}{C\left(S_{i}^{*}+m_{i}, Z_{i}\right)} \\
& =\frac{\beta C\left(S_{i}^{*}, Z_{i}\right)+C\left(e_{i}, Z_{i}\right)}{C\left(S_{i}^{*}, Z_{i}\right)+C\left(m_{i}, Z_{i}\right)}
\end{aligned}
$$

Our discussion of the mistakes in Karen and Sharon's reports of one another's schooling assumes that $C\left(e_{i}, Z_{i}\right)=C\left(m_{i}, Z_{i}\right)=0$. This in turn

## implies that

$$
\beta_{I V}=\beta \frac{C\left(S_{i}^{*}, Z_{i}\right)}{C\left(S_{i}^{*}, Z_{i}\right)}=\beta
$$

# This happy conclusion comes from our assumption that the only reason $Z_{i}$ is correlated with wages is because it's correlated with $S_{i}^{*}$. Since $S_{i}=S_{i}^{*}+m_{i}$, and $m_{i}$ is unrelated to $Z_{i}$, the usual IV miracle goes through. 

## po: That is severely cool. <br> Kung Fu Panda 2

[^13]The net effect of a 1-year experience increase is therefore

$$
(.081 \times 1)-(.0012 \cdot(2 x+1))=.08-.0024 x
$$

The first year of experience is therefore estimated to boost earnings by almost $8 \%$ while the tenth year of experience increases earnings by only about $5.6 \%$. In fact, the experience profile, as this relationship is called, flattens out completely after about 30 years of experience.
${ }^{4}$ Zvi Griliches, "Estimating the Returns to Schooling-Some Econometric Problems," Econometrica, vol. 45, no. 1, January 1977, pages 1-22.
${ }^{5}$ Attentive readers will notice that potential experience, itself a downstream consequence of schooling, also falls under the category of bad control. In principle, the bias here can be removed by using age and its square to instrument potential experience and its square. As in the studies referenced in the rest of this chapter, we might also simply replace the experience control with age, thereby targeting a net schooling effect that does not adjust for differences in potential experience.
${ }^{6}$ Orley Ashenfelter and Alan B. Krueger, "Estimates of the Economic Returns to Schooling from a New Sample of Twins," American Economic Review, vol. 84, no. 5, December 1994, pages 1157-1173, and Orley Ashenfelter and Cecilia Rouse, "Income, Schooling, and Ability: Evidence from a New Sample of Identical Twins," Quarterly Journal of Economics, vol. 113, no. 1, February

1998, pages 253-284.
${ }^{7}$ Estimates of this differenced model can also be obtained by adding a dummy for each family to an undifferenced model fit in a sample that includes both twins. Family dummies are like selectivity-group dummies in equation (2.2) in Chapter 2 and state dummies in equation (5.5) in Section 5.2. With only two observations per family, models estimated after differencing across twins within families to produce a single observation per family generate estimates of the returns to schooling identical to those generated by "dummying out" each family in a pooled sample that includes both twins.
${ }^{8}$ Daron Acemoglu and Joshua D. Angrist, "How Large Are Human-Capital Externalities? Evidence from Compulsory-Schooling Laws," in Ben S. Bernanke and Kenneth Rogoff (editors), NBER Macroeconomics Annual 2000, vol. 15, MIT Press, 2001, pages 9-59.
${ }^{9}$ Joshua D. Angrist and Alan B. Krueger, "Does Compulsory School Attendance Affect Schooling and Earnings?" Quarterly Journal of Economics, vol. 106, no. 4, November 1991, pages 979-1014.
${ }^{10}$ Kasey Buckles and Daniel M. Hungerman, "Season of Birth and Later Outcomes: Old Questions, New Answers," NBER Working Paper 14573, National Bureau of Economic Research, December 2008. See also John Bound, David A. Jaeger, and Regina M. Baker, who were the first to caution that IV estimates using QOB instruments might not have a causal interpretation in "Problems with Instrumental Variables Estimation When the Correlation between the Instruments and the Endogeneous Explanatory Variable Is Weak," Journal of the American Statistical Association, vol. 90, no. 430, June 1995, pages 443-450.
${ }^{11}$ For more on this point, see Joshua D. Angrist and Alan B. Krueger, "The Effect of Age at School Entry on Educational Attainment: An Application of Instrumental Variables with Moments from Two Samples," Journal of the American Statistical Association, vol. 87, no. 418, June 1992, pages 328-336.
${ }^{12}$ Damon Clark and Paco Martorell, "The Signaling Value of a High School Diploma," Journal of Political Economy, vol. 122, no. 2, April 2014, pages 282-318.

