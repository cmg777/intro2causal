"""Curated teaching content. Shared by the notebook and case-study page builders.

Edit the explicit lessons here; never select plot variables automatically.
Source URLs are included only after destination/content review (see verification report).
"""
from textwrap import dedent

CASES = {}
def case(key, title, question, keys, story, takeaway, prediction, caution, bridge, source, url=None):
    CASES[key] = dict(title=title, question=question, keys=keys.split(), story=story,
        takeaway=takeaway, prediction=prediction, caution=caution, bridge=bridge,
        source=source, sourceUrl=url, steps=[])

def step(key, title, question, explain, code, interact, interpret):
    CASES[key]['steps'].append(dict(title=title, question=question, explain=explain,
        code=dedent(code).strip(), interact=interact, interpret=interpret))

def practice(key, modify, task, hint1, hint2, solution, interpretation):
    CASES[key]['practice']=dict(modify=modify, task=task, hints=[hint1,hint2],
        solution=dedent(solution).strip(), interpretation=interpretation)

RAND='https://www.aeaweb.org/articles?id=10.1257/jep.27.1.197'
MIT='https://economics.mit.edu/people/faculty/josh-angrist/angrist-data-archive'
case('nhis_clean', 'Healthier people. Better insurance?',
 'Does having insurance explain why insured people report better health?', 'health insurance education family_income weight',
 'A health survey can reveal a striking gap without telling us what caused it. The 2009 National Health Interview Survey asked people about their health, insurance, and household circumstances. This teaching extract selects married adults ages 26–59 in households with an employed adult; it is not a picture of every American. Each row records one person, including a self-reported health score, schooling, and family income. Insurance was not randomly assigned. People with coverage may also have jobs, resources, or other advantages that shape their health. Start by comparing health distributions, then look at who belongs to each insurance group. The question becomes more interesting as the comparison becomes less simple: if the groups differ in several ways, how could we separate the contribution of insurance from those other differences?',
 'Compare health distributions, then look for differences that make a causal interpretation difficult.',
 'If insured people report better health, what are two explanations besides an effect of insurance?',
 'Health is an ordered response from 1 (poor) to 5 (excellent), not a clinical measurement. This selected household sample is not the entire NHIS. Initial summaries give each row equal weight.',
 'What would random assignment of insurance change about the comparison you just made?',
 'National Center for Health Statistics, 2009 NHIS data release',
 'https://archive.cdc.gov/www_cdc_gov/nchs/nhis/nhis_2009_data_release.htm')
case('rand_balance','Before the experiment begins',
 'Were people assigned to different insurance plans comparable at baseline?', 'plan_type age education health_index',
 'Imagine trying to learn whether free medical care improves health. Comparing people who buy different plans would mix the effects of insurance with the reasons they chose those plans. The RAND Health Insurance Experiment took a different approach: families were randomly assigned to plans with different cost-sharing arrangements. This file contains baseline characteristics from the experiment, including age, schooling, income, and health measures. Each row is a participant, while family members share an assignment and may resemble one another. Before examining later outcomes, we can ask whether the plan groups started out looking similar. Random assignment does not guarantee identical averages in a finite sample, and missing records can complicate the picture. This investigation develops the habit of checking the starting point before interpreting an apparent treatment effect.',
 'Look for baseline similarities and differences across plans, while keeping missing records visible.',
 'Would random assignment make every plan group have exactly the same average age? Why?',
 'Plan type is missing for some stored rows. Comparisons use only known plan types and available values for the plotted outcome. Participants within a family are not independent assignments.',
 'Why does an outcome difference become more informative when the groups were comparable before treatment?',
 'Aron-Dine, Einav and Finkelstein (2013), The RAND Health Insurance Experiment, Three Decades Later',RAND)
case('rand_utilization','When care costs less, do people use more?',
 'How does healthcare use differ across randomly assigned insurance plans?', 'plan_type visits total_expenses admissions',
 'An insurance plan changes the price a family faces when someone needs care. Lower prices may encourage useful treatment, but they can also increase spending without producing equal improvements in health. The RAND experiment assigned families to plans ranging from free care to substantial cost sharing. This extract joins healthcare-use records and annual spending, with expenses expressed in constant 1991 dollars. A row represents a participant-year, so the same person can contribute more than one record. Most people may spend relatively little while a small number incur very large expenses. That makes this a useful case for learning why a mean alone can be misleading. We will inspect the distribution, compare visits across plans, and ask what a spending difference does—and does not—tell us about the value of medical care.',
 'Explore skewed spending and compare visits and expenses across plans.',
 'Could two plans have similar typical spending but quite different average spending?',
 'Rows are participant-years. Spending is in constant 1991 dollars. Repeated people and family assignments matter for inference; this lesson makes descriptive comparisons only.',
 'If free care increases visits, what additional outcomes would you need to decide whether it improves health?',
 'Aron-Dine, Einav and Finkelstein (2013), The RAND Health Insurance Experiment, Three Decades Later',RAND)
case('rand_health_outcomes','More care. Better health?',
 'How do measured health outcomes compare across insurance plans?', 'plan_type health_index blood_pressure cholesterol',
 'Using more healthcare and becoming healthier are different outcomes. The RAND Health Insurance Experiment makes that distinction tangible: families were assigned different cost-sharing plans, and researchers collected health measures as well as spending records. This extract contains exit measures such as a general health index, blood pressure, and cholesterol. A row represents a participant in the stored exit-measure file, but some rows lack the measurements needed for a particular comparison. Different outcomes also have different scales and interpretations; higher values are not always better. We will first make the available evidence visible, then compare the distributions of selected health measures across plans. The aim is to learn how to ask a precise outcome question and avoid turning one descriptive chart into a broad claim about every participant or every dimension of health.',
 'Compare health outcomes and check whether missing measurements limit the comparison.',
 'If a plan produces more medical visits, must it improve every health measure?',
 'Outcome availability differs across measures. Do not combine health indices, blood pressure, and cholesterol on one numeric scale. These plots are not clinical advice or estimates of statistical significance.',
 'How could missing exit measurements weaken a comparison that began with random assignment?',
 'Aron-Dine, Einav and Finkelstein (2013), The RAND Health Insurance Experiment, Three Decades Later',RAND)
case('mdve_clean','Assigned is not always delivered',
 'When officers were assigned a response, how often was that response delivered?', 'assigned delivered',
 'In Minneapolis in 1981–1982, researchers studied police responses to eligible misdemeanor domestic assault incidents. Officers were assigned one of three responses: arrest, advice, or separating the parties. The wider study asked whether these responses affected repeat violence. In practice, an assigned response was not always the response delivered. This teaching extract contains 314 records with only those two categorical fields; the original study involved 330 cases, and the extract does not contain subsequent violence outcomes. We can therefore investigate how assignment translated into action, but cannot estimate whether arrest reduced repeat violence from this file. A count chart and a cross-tabulation make the distinction visible. It is a concrete introduction to noncompliance: even when an assignment is randomized, the treatment actually received may reflect additional decisions and circumstances.',
 'Trace the difference between assigned and delivered responses, then identify the evidence still missing.',
 'Would comparing people actually arrested with people not arrested preserve the original random assignment?',
 'This extract has no recidivism outcome. Its 314 records must not be described as all 330 study cases. Use respectful language: these records concern serious harm to people.',
 'Why might assigned response be a more credible starting point than delivered response when investigating an arrest effect?',
 'Sherman and Berk (1984), The Minneapolis Domestic Violence Experiment',
 'https://www.ojp.gov/library/publications/minneapolis-domestic-violence-experiment')
case('mlda_clean','What changes on a twenty-first birthday?',
 'Do mortality patterns change at the age when alcohol becomes legally available?', 'agecell all mva suicide over21',
 'A birthday is an ordinary passage of time, but turning 21 in the United States also changes legal access to alcohol. Carpenter and Dobkin used this threshold to investigate the relationship between alcohol access and mortality. The teaching file records mortality rates for narrow age cells around the cutoff rather than individual people. Each point on a chart is therefore an aggregate, measured in deaths per 100,000 person-years. The file contains both actual age and age centered on 21; confusing the two would put the policy threshold in the wrong place. We will plot actual age, compare causes of death, and zoom in near the birthday. The central reasoning challenge is to distinguish a gradual age pattern from an abrupt change at the policy boundary, while asking what else could change at precisely the same age.',
 'Use an age threshold to ask when nearby observations might offer a useful comparison.',
 'Would you expect mortality to change smoothly with age, or jump at a particular birthday?',
 'Use agecell for actual age; age is centered on 21. Rates describe age cells, not individual death probabilities. A visible jump alone does not establish the assumptions of a causal design.',
 'What must be true about other influences near age 21 for the cutoff to help isolate legal alcohol access?',
 'Carpenter and Dobkin (2009), The Effect of Alcohol Consumption on Mortality',
 'https://www.aeaweb.org/articles?id=10.1257/app.1.1.164')
case('banks_clean','Two districts. One banking crisis.',
 'Did different Federal Reserve responses help banks survive the Great Depression?', 'year bib6 bib8 counterfactual',
 'During the Great Depression, Mississippi straddled two Federal Reserve districts that responded differently to banking distress. Richardson and Troost studied this boundary to investigate whether emergency lending helped banks survive. This teaching extract gives six July 1 snapshots of the number of banks still in business in each district. These are operating-bank counts, not counts of failures, and the districts did not start with the same number of banks. The file also supplies a constructed path for the sixth district based on the eighth district’s changes from 1930. That path is a counterfactual illustration, not another observed district. By looking first at levels and then at changes, we can ask why a before-and-after comparison might be insufficient and what a comparison district contributes to the argument. Six observations are enough for an important question, but not for unlimited historical conclusions.',
 'Compare changes in operating banks and separate observed history from a constructed counterfactual.',
 'If both districts lose banks, could lending still have helped one district?',
 'There are only six annual snapshots. bib6 and bib8 count banks in business. The supplied counterfactual holds the 1930 district gap fixed; it is not observed evidence of what would certainly have happened.',
 'What would make the eighth district a credible guide to how the sixth would have changed without intervention?',
 'Richardson and Troost (2009), Monetary Intervention Mitigated Banking Panics during the Great Depression',
 'https://www.economics.uci.edu/files/docs/faculty_review/richardson_troost_2009_jpe.pdf')
case('deaths_clean','A policy changes. A trend continues.',
 'How do drinking-age policy and young-adult mortality move across states and years?', 'year state dtype mrate legal',
 'When states change a drinking-age law, many other things are changing too: road safety, travel, economic conditions, and public attitudes. A state-by-year panel allows us to follow these overlapping changes rather than compare just two national averages. This prepared teaching extract contains death rates for young adults, a legal-access measure, and population information, repeated for several causes of death. Each row describes one state, year, and cause, not one person. The chapter identifies the population as ages 18–20, although the repository does not reproduce the entire upstream cleaning process. We will keep causes separate, follow selected state trajectories, and put policy changes alongside mortality trends. The point is to see why an apparent policy association raises further questions about timing and comparison groups before it becomes a causal claim.',
 'Read a panel as repeated state observations and investigate policy timing without pooling incompatible outcomes.',
 'If mortality falls after a law changes, what other trend could explain the decline?',
 'Select one dtype before averaging rates. legal measures the share legally allowed to drink, not a randomized binary assignment. Population weighting changes which states contribute most.',
 'How could states with different policy timing help distinguish a policy effect from a shared national trend?',
 'Chapter 5 MLDA teaching panel; Du Mouchel, Williams and Zador (1987), Raising the Alcohol Purchase Age: Its Effects on Fatal Motor Vehicle Crashes in Twenty-Six States')
case('qob_clean','Can a birthday shape schooling?',
 'Why might quarter of birth be related to schooling, and what could that teach us about earnings?', 's lnw qob yob',
 'People with more schooling often earn more, but that pattern combines education with the reasons people stay in school. Angrist and Krueger investigated a different source of variation: birth timing interacting with school-entry and compulsory-attendance rules. This extract contains men from the 1980 U.S. Census, with schooling, log weekly earnings, and quarter and year of birth. It is the largest file in the collection, so plotting every person at once can conceal rather than reveal structure. We will begin with summaries that use all relevant rows, then compare birth-quarter patterns within cohorts. The differences may be small; reading their size carefully is part of the lesson. A birthday does not automatically become a valid instrument. The investigation ends by asking what assumptions connect birth timing, schooling, and earnings.',
 'Discover a small schooling pattern within a large census extract and ask what would make it useful for causal reasoning.',
 'Would you expect people born in different quarters of the same year to have similar schooling?',
 'lnw is log weekly earnings, not dollars. yob uses two-digit birth-year codes. Group means use all available rows; any display sample must be identified.',
 'Besides changing schooling, could quarter of birth be related to earnings through another route?',
 'Angrist and Krueger (1991), Does Compulsory School Attendance Affect Schooling and Earnings? Author data archive',MIT)
case('twins_clean','A comparison within the family',
 'Does the schooling–wage pattern look different when we compare twins?', 'educ lwage first deduc dlwage',
 'Comparing unrelated people leaves many possible explanations for a schooling–earnings association. Twins offer a way to hold some family background and inherited characteristics more nearly constant. The Twinsburg research collected information about education and wages, including reports of schooling from both twins. This prepared extract contains individual observations and supplied within-pair differences. It does not give us a general-purpose pair identifier, so we must follow the chapter’s instruction to use records marked first when examining those differences. We will contrast the individual pattern with a chart of schooling and wage differences within pairs, then inspect disagreement between schooling reports. Similar upbringing does not eliminate every difference between twins, and reported schooling can contain error. This case shows both the appeal of a closer comparison and the new questions it introduces.',
 'Compare individuals with within-pair differences, and see why measurement quality matters.',
 'What influences on earnings might twins share, and what influences might still differ?',
 'Use first == 1 once per pair for supplied differences. Do not infer pairs from row order. lwage and dlwage are log-wage quantities, not dollar wages.',
 'Why might removing shared background make measurement error in schooling differences more important?',
 'Twinsburg studies: Ashenfelter and Krueger (1994); Ashenfelter and Rouse (1998). Book replication resource',
 'https://www.masteringmetrics.com/resources-post/chapter-6-table-6-2/')
case('childlabor_clean','When the law keeps children in school',
 'How do schooling and wages vary across cohorts exposed to different schooling requirements?', 'yob indEduc lnwkwage cl7 cl8 cl9',
 'School attendance is shaped by family circumstances as well as legal requirements. Acemoglu and Angrist studied historical schooling laws to investigate education and earnings. This teaching file is already aggregated: a row represents a birth-state, birth-year, and census-year cell, with average schooling and log weekly wages. The law indicators distinguish required-schooling categories associated with child-labor restrictions; they must not be interpreted as ages for entering school. This distinction matters because an appealing story can be wrong even when the code runs. We will compare cohort patterns and law categories while keeping the aggregate observation unit visible. States and cohorts differ in many ways besides laws, so these charts are a starting point for asking what variation might support an instrument, not a direct estimate of a law’s causal effect.',
 'Read aggregate cells carefully and explore how legal requirements might create schooling variation.',
 'Would states with stricter schooling requirements necessarily be comparable in other ways?',
 'cl7, cl8 and cl9 identify required-schooling categories (7, 8, and 9 or more years), not school-entry ages. weight is a source sample-line analysis weight; n is a stored cell count. Equal-cell summaries are explicitly unweighted.',
 'What differences between states and birth cohorts would need attention before treating a law as a source of causal variation?',
 'Acemoglu and Angrist (2000), How Large Are Human-Capital Externalities? Evidence from Compulsory Schooling Laws; author archive',MIT)
case('sheepskin_clean','What is a diploma worth?',
 'Does crossing an exit-exam threshold change diploma receipt and later earnings?', 'minscore receivehsd avgearnings n',
 'A diploma may signal skills to employers, but graduates also tend to have more schooling and different backgrounds than nongraduates. Clark and Martorell studied students near a Texas high-school exit-exam passing threshold to make a closer comparison. This extract contains score-bin averages rather than individual student records. Each bin records a diploma-receipt rate, average later earnings, and the number of students represented. Passing the exam does not translate perfectly into receiving a diploma, which makes it useful to examine the two links separately: score to credential, and score to earnings. We will mark the passing threshold, inspect both outcomes, and look at how much information supports each point. A large visual difference in a small bin deserves different scrutiny from a stable pattern supported by many students.',
 'Separate passing an exam, receiving a diploma, and earning more, while checking bin sizes.',
 'Would a jump in diploma receipt necessarily imply a jump in earnings?',
 'minscore is distance from the passing threshold. Each row is a score bin; n counts students, while person_years supports earnings observations. Do not average bins as though they were individual students.',
 'Why must a design first establish that crossing the threshold actually changes the probability of receiving a diploma?',
 'Clark and Martorell (2014), The Signaling Value of a High School Diploma')
case('synthetic_ovb','The variable you almost overlooked',
 'How can ability complicate the relationship between schooling and earnings?', 'schooling earnings ability occupation',
 'Real data rarely reveal every reason that people choose more education. This teaching simulation gives us an advantage: the data-generating code includes ability, schooling, occupation, and log earnings, so we can inspect relationships that might be hidden in practice. Each row is a simulated person. Ability influences both schooling and earnings, while occupation is partly a consequence of schooling and provides another route to earnings. These roles are different: a variable that precedes schooling is not interchangeable with one that follows it. We will start with the familiar schooling–earnings pattern, color observations by ability, and compare it with the schooling–occupation relationship. The numbers are generated for learning, not evidence about an actual population. Their value is that they let us reason explicitly about why adding a variable to an analysis can change what question we are answering.',
 'Visualize a confounder and distinguish it from a variable that lies on a causal pathway.',
 'If ability raises both schooling and earnings, would the raw schooling–earnings pattern exaggerate the effect of schooling?',
 'The column earnings contains simulated log earnings. Occupation is generated after schooling and acts as a mediator. The generator includes clipping and rounding, so simplistic exact-effect claims are inappropriate.',
 'Why might controlling for occupation remove part of the schooling effect you wanted to learn about?',
 'Repository teaching simulation, code/python/ch6/generate_synthetic.py',
 'https://github.com/cmg777/intro2causal/blob/main/code/python/ch6/generate_synthetic.py')
case('synthetic_rct','A scholarship offer changes the comparison',
 'What does randomized scholarship assignment reveal about schooling and earnings?', 'scholarship ability schooling earnings',
 'Suppose a scholarship is offered by lottery. Recipients may spend longer in school, but they do not all acquire the same amount of education. This teaching simulation separates the randomized offer from the schooling that follows it. Each generated person has an ability score, a scholarship assignment, years of schooling, and log earnings. Ability affects schooling and earnings, while the scholarship changes schooling without being selected on ability. We will compare ability distributions across the lottery groups, examine how their schooling differs, and then inspect earnings. That sequence helps avoid a common leap: an effect of offering a scholarship is not automatically an effect per additional year of education. Because the relationships are constructed, this is a safe place to explore the logic before encountering the complications of a real experiment.',
 'Follow a randomized offer through schooling and earnings, keeping assignment distinct from treatment received.',
 'Should scholarship recipients have systematically higher ability before receiving the offer?',
 'This is simulated data, not an actual scholarship evaluation. earnings contains log earnings. Schooling is clipped and rounded by the generator.',
 'What additional assumptions would let a randomized scholarship offer help identify the effect of schooling itself?',
 'Repository teaching simulation, code/python/ch6/generate_synthetic.py',
 'https://github.com/cmg777/intro2causal/blob/main/code/python/ch6/generate_synthetic.py')
case('synthetic_did','A reform arrives halfway through the story',
 'How do schooling and earnings trajectories differ around a simulated reform?', 'year treated post avg_schooling avg_earnings',
 'A policy often arrives after years of change are already underway. This simulation follows 20 states from 1995 to 2014, with ten adopting a schooling reform in 2005. Each row is a state-year average. The generator gives states different starting levels, a shared underlying time trend, and random fluctuations; after adoption, it adds a schooling increase and a change in average log earnings to treated states. We will first inspect the trajectories, then compare schooling patterns and changes relative to a common pre-reform year. Looking at changes helps separate starting differences from subsequent movement. In this artificial world, we can inspect the assumptions written into the generator. In an actual policy study, we would have to argue for those assumptions using evidence and institutional knowledge rather than knowing them by construction.',
 'Compare levels and changes, then explain the counterfactual role of the comparison states.',
 'If treated states start with lower earnings, does that alone make them an unsuitable comparison?',
 'Rows are repeated state-years, not independent people. avg_earnings is an average log-earnings outcome. Similar pre-trends are evidence to consider, not proof of future parallel trends.',
 'What would threaten the claim that comparison states describe how treated states would have changed without reform?',
 'Repository teaching simulation, code/python/ch6/generate_synthetic.py',
 'https://github.com/cmg777/intro2causal/blob/main/code/python/ch6/generate_synthetic.py')

# All transformations below are intentionally explicit and teachable.
step('nhis_clean','A health gap is a distribution','Are the two groups spread across health categories in the same way?',
 'A count answers how many; a percentage makes groups of different sizes comparable. groupby collects rows sharing the same labels. size counts those rows. Dividing by each group total turns counts into percentages.',
 '''health_counts = df.groupby(["insurance", "health"]).size().reset_index(name="people")
health_counts["percent"] = 100 * health_counts["people"] / health_counts.groupby("insurance")["people"].transform("sum")
health_counts["coverage"] = health_counts["insurance"].map({0: "Uninsured", 1: "Insured"})
fig = px.bar(health_counts, x="health", y="percent", color="coverage", barmode="group", labels={"health": "Health score: 1 poor → 5 excellent", "percent": "People within coverage group (%)", "coverage": "Insurance"}, title="How people describe their health")''',
 'Hover over health scores 1 and 5. Compare the percentages, not just the color. Toggle a group in the legend.',
 'Describe where each distribution is concentrated. A health gap is an association; the chart does not tell us why coverage and health differ.')
step('nhis_clean','Who has insurance?','Do the groups also differ in education?',
 'A box plot summarizes a distribution: the box covers its middle half and the line inside marks its median, the middle value. We hide individual points to keep this large sample readable.',
 '''people = df.copy()
people["coverage"] = people["insurance"].map({0: "Uninsured", 1: "Insured"})
fig = px.box(people, x="coverage", y="education", color="coverage", points=False, labels={"coverage": "Insurance", "education": "Years of education"}, title="Schooling differs across insurance groups")''',
 'Hover over each box to inspect its median and quartiles. Would the same health comparison be persuasive if schooling differed substantially?',
 'Education is one observed difference that could help explain the health gap. It is not a complete list of confounders, and the box plot does not estimate their contributions.')
step('nhis_clean','Resources behind the comparison','How different are typical family incomes?',
 'The median is less sensitive to very high incomes than the mean. Here we calculate one median per coverage group. Family income describes a household resource even though the stored rows are people.',
 '''income = people.groupby("coverage", as_index=False)["family_income"].median()
fig = px.bar(income, x="coverage", y="family_income", color="coverage", labels={"coverage": "Insurance", "family_income": "Median family income (source dollars)"}, title="Another difference to explain")''',
 'Hover to read the income values. Name a way family resources might affect both insurance and health.',
 'The insured–uninsured comparison bundles insurance with other circumstances. These data invite a stronger research design; they do not isolate an insurance effect.')
practice('nhis_clean','In the education box plot, change education to age and update the axis label. Predict which group will be older.',
 'Make a chart of mean health by coverage group. Then explain why its simplicity could be misleading.', 'Start with the people table, which already has readable coverage labels.', 'Use people.groupby("coverage", as_index=False)["health"].mean(), then px.bar.',
 '''means = people.groupby("coverage", as_index=False)["health"].mean()
fig = px.bar(means, x="coverage", y="health", color="coverage", labels={"coverage": "Insurance", "health": "Mean health score (1–5)"}, title="A useful summary, not a causal effect")
fig.show()''', 'A mean compresses an ordered health distribution into one number. The earlier schooling and income charts show why that difference cannot be attributed to insurance alone.')

for key,measure,title in [('rand_balance','age','Age before treatment'),('rand_health_outcomes','health_index','Health at the end of the experiment')]:
 step(key,'First, count the available evidence','How many usable records support each plan comparison?',
  'We keep rows with a known plan and count available values for this outcome. count excludes missing measurements. A small bar could mean fewer participants or more missing outcomes, so it is useful to check both.',
  f'''coverage = plans.groupby("plan", as_index=False).agg(records=("plan", "size"), observed=("{measure}", "count"))
coverage["missing"] = coverage["records"] - coverage["observed"]
coverage_long = coverage.melt(id_vars="plan", value_vars=["observed", "missing"], var_name="availability", value_name="participants")
fig = px.bar(coverage_long, x="plan", y="participants", color="availability", labels={{"plan": "Assigned plan", "participants": "Participant records", "availability": "{measure} availability"}}, title="What evidence is available?")''',
  'Hover over the observed and missing segments. Missing measurements are not zero-valued outcomes.',
  'Keep the availability chart beside your substantive comparison. Different sample sizes and missingness can affect how confidently we compare groups.')
 step(key,'Look beyond a single average',f'How does {measure.replace("_"," ")} vary within and across plans?',
  'A box contains the middle half of the available values; its central line is the median. The whiskers extend into the tails. We suppress individual points to make the groups readable.',
  f'''fig = px.box(plans, x="plan", y="{measure}", color="plan", points=False, labels=labels, title="{title}")''',
  'Hover over the boxes. Compare the differences between medians with the spread within each plan.',
  'Overlapping distributions remind us that people vary within every plan. A descriptive difference is not a significance test and is not automatically evidence of a large effect.')
 other='education' if key=='rand_balance' else 'blood_pressure'
 step(key,'Ask whether the picture travels',f'Does the comparison look similar for {other.replace("_"," ")}?',
  'groupby gathers the known-plan records; mean averages available values within each plan. The source rows used can differ from the previous chart because this outcome has its own missing values.',
  f'''means = plans.groupby("plan", as_index=False)["{other}"].mean()
fig = px.bar(means, x="plan", y="{other}", color="plan", labels=labels, title="A second measure, a separate comparison")''',
  'Hover for exact means. Use the variable guide to decide what a higher value means for this measure.',
  'Do not generalize from one outcome to all outcomes. Ask whether the records are comparable, whether the measure is relevant, and what the research design can justify.')
 practice(key,f'Change the box plot outcome from {measure} to '+('health_index' if key=='rand_balance' else 'cholesterol')+'. Read its definition before interpreting it.',
  'Calculate and plot the number of nonmissing education records per plan.' if key=='rand_balance' else 'Calculate and plot the number of nonmissing cholesterol records per plan.',
  'Use the plans table, which excludes unknown plan types.', 'groupby(...).count() counts nonmissing observations for your chosen variable.',
  f'''counts = plans.groupby("plan", as_index=False)["{'education' if key=='rand_balance' else 'cholesterol'}"].count()
fig = px.bar(counts, x="plan", y="{'education' if key=='rand_balance' else 'cholesterol'}", labels={{"plan": "Assigned plan", "{'education' if key=='rand_balance' else 'cholesterol'}": "Available participant records"}}, title="Check the denominator")
fig.show()''',
  'Counts tell you how much available evidence lies behind a comparison. They do not tell you whether missingness is unrelated to treatment or health.')
step('rand_utilization','Meet the long tail','Is most spending near the average, or is the distribution skewed?',
 'A histogram counts observations inside value intervals. For spending, a few very large amounts can stretch the axis. Zoom to inspect the dense region, then double-click to restore the full distribution.',
 '''fig = px.histogram(df, x="total_expenses", nbins=60, labels=labels, title="A small number of expensive participant-years")''',
 'Drag across the lower-spending part of the chart to zoom. Reset and notice how far the tail extends.',
 'The long right tail means the mean can lie well above the spending of a typical participant-year. Do not delete large values merely to make the picture neater.')
step('rand_utilization','Follow use, not only money','How do average medical visits compare across plans?',
 'The mean is total visits divided by participant-years with a recorded value. It describes use, not the health benefit of those visits.',
 '''visits = plans.groupby("plan", as_index=False)["visits"].mean()
fig = px.bar(visits, x="plan", y="visits", color="plan", labels=labels, title="Average visits by assigned plan")''',
 'Hover to compare free care with each cost-sharing plan. State the unit: visits per participant-year.',
 'Random assignment makes the plan contrast interesting, but these unadjusted summaries do not account for all analysis restrictions or repeated observations.')
step('rand_utilization','Two summaries, two questions','Do mean and median spending tell the same story?',
 'agg computes several summaries at once. melt reshapes those summaries into a long table: one row for each plan and summary type, which Plotly can color.',
 '''spending = plans.groupby("plan")["total_expenses"].agg(["mean", "median"]).reset_index()
spending_long = spending.melt(id_vars="plan", var_name="summary", value_name="dollars")
fig = px.bar(spending_long, x="plan", y="dollars", color="summary", barmode="group", labels={"plan": "Assigned plan", "dollars": "Annual spending (1991 dollars)", "summary": "Summary"}, title="The mean and the typical participant-year")''',
 'Toggle mean or median in the legend. Does your comparison depend on which summary you choose?',
 'The mean captures total resource use per row; the median locates the middle row. Neither tells us whether extra care was beneficial.')
practice('rand_utilization','In the visits comparison, replace visits with admissions and update the title.',
 'Make a box plot comparing total expenses across plans, hiding individual points.', 'Use plans, plan, and total_expenses.', 'px.box(..., points=False) keeps the display compact.',
 '''fig = px.box(plans, x="plan", y="total_expenses", color="plan", points=False, labels=labels, title="Spending variation within plans")
fig.show()''','The boxes show that a plan-level mean hides substantial variation. Keep the full data and explain any zoom used for display.')
step('mdve_clean','Count the assigned responses','Were all three assignments equally common in the stored extract?',
 'value_counts counts category labels. reset_index gives the counts column names so we can plot them. These are cases in this extract, not the entire source study.',
 '''counts = df["assigned"].value_counts().rename_axis("assigned").reset_index(name="cases")
fig = px.bar(counts, x="assigned", y="cases", color="assigned", labels={"assigned": "Assigned response", "cases": "Cases in extract"}, title="The starting assignment")''',
 'Hover over each bar. Is equal random-assignment probability the same thing as exactly equal realized counts?',
 'Finite samples can have unequal counts. Counts alone cannot show whether assignment was implemented correctly or whether omitted cases differ.')
step('mdve_clean','Follow assignment into action','For each assigned response, what was actually delivered?',
 'crosstab builds a table of category combinations. normalize="index" divides each row by its own total, so each assigned-response row adds to 100%.',
 '''shares = pd.crosstab(df["assigned"], df["delivered"], normalize="index") * 100
fig = px.imshow(shares, text_auto=".1f", zmin=0, zmax=100, color_continuous_scale="Blues", labels={"x": "Delivered response", "y": "Assigned response", "color": "Within assignment (%)"}, title="Where assignment and action diverge")''',
 'Hover over a diagonal cell (matching responses), then an off-diagonal cell. Explain both denominators.',
 'Off-diagonal cells show noncompliance. A comparison based on delivered responses can therefore sort cases differently from the randomized assignment.')
step('mdve_clean','Summarize the mismatch','Which assignments were most often delivered as assigned?',
 '== compares two values and returns True or False. The mean of these values is a proportion because True counts as 1 and False as 0.',
 '''compliance = df.assign(matched=df["assigned"] == df["delivered"])
matched = compliance.groupby("assigned", as_index=False)["matched"].mean()
matched["percent"] = 100 * matched["matched"]
fig = px.bar(matched, x="assigned", y="percent", labels={"assigned": "Assigned response", "percent": "Delivered as assigned (%)"}, title="Compliance depends on the assignment")
fig.update_yaxes(range=[0, 100])''',
 'Identify the smallest match rate. Describe the result without claiming a cause of noncompliance.',
 'You have measured assignment fidelity, not the effect on violence. The absence of an outcome variable sets a firm boundary on this investigation.')
practice('mdve_clean','Change normalize="index" to normalize="columns" in the heatmap. Explain the new denominator before interpreting it.',
 'Plot the distribution of delivered responses only among cases assigned to Separate.', 'Filter with df[df["assigned"] == "Separate"].', 'Count delivered values in the filtered table, then use px.bar.',
 '''separate = df[df["assigned"] == "Separate"]
counts = separate["delivered"].value_counts().rename_axis("delivered").reset_index(name="cases")
fig = px.bar(counts, x="delivered", y="cases", labels={"delivered": "Delivered response", "cases": "Cases assigned Separate"})
fig.show()''','The bars follow one assignment group into its delivered responses. They do not show which response worked best.')
step('mlda_clean','Locate the policy boundary','What happens to all-cause mortality near age 21?',
 'A scatter plot keeps the age-cell observations visible. We draw a vertical guide at actual age 21; the guide is a policy threshold, not a fitted causal effect.',
 '''fig = px.scatter(df, x="agecell", y="all", labels=labels, title="Mortality around the twenty-first birthday")
fig.add_vline(x=21, line_dash="dash", line_color="#7c3aed")''',
 'Hover just below and above 21. Describe the local pattern rather than comparing the youngest and oldest cells.',
 'A local change suggests a question for regression discontinuity. Whether it identifies an alcohol-access effect depends on other influences being sufficiently smooth at the boundary.')
step('mlda_clean','Ask which outcomes move','Do different causes of death have the same age pattern?',
 'melt turns separate outcome columns into one rate column and one cause label. Separate panels preserve each cause’s shape without confusing the measures.',
 '''causes = df.melt(id_vars="agecell", value_vars=["mva", "suicide", "internal"], var_name="cause", value_name="rate")
fig = px.scatter(causes, x="agecell", y="rate", facet_col="cause", facet_col_wrap=2, labels={"agecell": "Age (years)", "rate": "Deaths per 100,000 person-years"}, title="Compare causes of death")
fig.add_vline(x=21, line_dash="dash")''',
 'Compare motor-vehicle (mva), suicide, and internal causes. Do all panels suggest an equally abrupt change?',
 'A design should make sense for specific outcomes. Different cause patterns can help investigate mechanisms, but do not by themselves eliminate alternative explanations.')
step('mlda_clean','Change the window','Does the pattern survive a closer look at the cutoff?',
 'between selects observations in a stated interval. A smaller window gives a more local comparison but fewer data points.',
 '''near = df[df["agecell"].between(20.5, 21.5)]
fig = px.scatter(near, x="agecell", y="all", labels=labels, title="A one-year window around the threshold")
fig.add_vline(x=21, line_dash="dash")''',
 'Count how many points remain on each side. Compare this view with the full age range.',
 'Choosing a window involves a tradeoff between local comparability and information. Zooming is a diagnostic, not a substitute for estimating and checking a research design.')
practice('mlda_clean','Change the window to 20.75–21.25 and notice how much information is lost.',
 'Plot motor-vehicle mortality within ages 20–22 and mark age 21.', 'Filter using agecell, not the centered age column.', 'Use px.scatter(..., y="mva") and add_vline(x=21).',
 '''near = df[df["agecell"].between(20, 22)]
fig = px.scatter(near, x="agecell", y="mva", labels=labels)
fig.add_vline(x=21, line_dash="dash")
fig.show()''','Describe a visible pattern cautiously. You cannot infer an individual person’s risk or rule out every coincident change from these cells alone.')
step('banks_clean','Begin with observed history','How many banks remained in business in each district?',
 'The data are sorted by year before drawing lines. A line joins annual snapshots; it does not reveal what happened on every intervening day.',
 '''history = df.sort_values("year").melt(id_vars="year", value_vars=["bib6", "bib8"], var_name="district", value_name="banks")
history["district"] = history["district"].map({"bib6": "6th district", "bib8": "8th district"})
fig = px.line(history, x="year", y="banks", color="district", markers=True, labels={"year": "July 1 snapshot", "banks": "Banks in business", "district": "District"}, title="Operating banks during the crisis")''',
 'Hover over 1930 and 1931. Compare starting levels and subsequent movement separately.',
 'Fewer operating banks is a decline in this count. It is not a direct count of failures, and the starting difference makes a simple level comparison uninformative about policy.')
step('banks_clean','Put the starting point on equal footing','How did each district change relative to 1930?',
 'Subtracting the 1930 count within each district gives a change measured in banks. A zero indicates the baseline, not zero banks.',
 '''baseline = history[history["year"] == 1930].set_index("district")["banks"]
history["change"] = history["banks"] - history["district"].map(baseline)
fig = px.line(history, x="year", y="change", color="district", markers=True, labels={"year": "Year", "change": "Change in banks since 1930", "district": "District"}, title="Compare changes, not just levels")
fig.add_hline(y=0, line_dash="dot")''',
 'Compare how far each line falls after 1930. Both can fall while one falls less.',
 'Different declines motivate a differences-in-differences comparison. They do not prove that the two districts would have followed the same path without intervention.')
step('banks_clean','Make the assumption visible','How does the supplied counterfactual compare with the observed sixth district?',
 'The counterfactual is constructed from the eighth district’s movement and the 1930 gap. We draw it with a different line style to distinguish assumption from observation.',
 '''paths = df.melt(id_vars="year", value_vars=["bib6", "counterfactual"], var_name="path", value_name="banks")
paths["path"] = paths["path"].map({"bib6": "Observed 6th district", "counterfactual": "Constructed counterfactual"})
fig = px.line(paths, x="year", y="banks", color="path", line_dash="path", markers=True, labels={"year": "Year", "banks": "Banks in business", "path": "Path"}, title="Observed and assumed paths")''',
 'Toggle the counterfactual off, then on. Which line is observed? Which depends on an assumption?',
 'The gap illustrates the question the design asks. Calling it a policy effect requires historical support for the comparison, not just arithmetic.')
practice('banks_clean','Change the baseline year in the change chart to 1929. Explain why the displayed changes move.',
 'Calculate and plot observed sixth-district banks minus the supplied counterfactual for each year.', 'Create a column with df["bib6"] - df["counterfactual"].', 'Use a bar plot with year on x and the new gap on y.',
 '''gaps = df.assign(gap=df["bib6"] - df["counterfactual"])
fig = px.bar(gaps, x="year", y="gap", labels={"year": "Year", "gap": "Observed minus counterfactual (banks)"})
fig.show()''','The difference is relative to the supplied assumed path. It is not a count directly observed as banks saved by lending.')
step('deaths_clean','Follow the same states over time','Do state mortality trends look alike?',
 'We select all-cause deaths before comparing rates. The three state codes below are illustrative comparisons, not a selected treatment and control design. Sorting by year keeps lines in time order.',
 '''allcause = df[df["dtype"] == "all"].copy()
selected = allcause[allcause["state"].isin([1, 6, 48])].sort_values("year")
selected["state_label"] = selected["state"].map({1: "Alabama", 6: "California", 48: "Texas"})
fig = px.line(selected, x="year", y="mrate", color="state_label", markers=True, labels={"year": "Year", "mrate": "Deaths per 100,000 (ages 18–20)", "state_label": "State"}, title="Different places, different trajectories")''',
 'Toggle a state in the legend. Look for both level differences and different slopes.',
 'A shared downward trend could make a before/after policy comparison misleading. The chosen states illustrate heterogeneity; they are not automatically valid controls.')
step('deaths_clean','Put policy timing on the page','When does legal access change in these same states?',
 'legal is a share between 0 and 1. Multiplying by 100 displays a percentage. It measures policy access for the age group, not whether each person drinks.',
 '''selected["legal_percent"] = 100 * selected["legal"]
fig = px.line(selected, x="year", y="legal_percent", color="state_label", markers=True, labels={"year": "Year", "legal_percent": "Share legally allowed to drink (%)", "state_label": "State"}, title="Policy timing differs too")
fig.update_yaxes(range=[0, 100])''',
 'Locate a policy change and compare its year with the mortality chart. Does visual coincidence settle the causal question?',
 'Changes at different dates can help a panel design, but policy choices may respond to circumstances that also affect mortality.')
step('deaths_clean','A pooled pattern can hide a panel','What disappears when time and place are pooled?',
 'Each dot is now a state-year for all-cause mortality. Color shows calendar year, so we can see whether a simple policy association also reflects time.',
 '''fig = px.scatter(allcause, x="legal", y="mrate", color="year", hover_data=["state"], opacity=0.5, labels=labels, title="One scatter plot mixes many comparisons")''',
 'Hover to identify the state and year behind a point. Check whether early and late years occupy different regions.',
 'A pooled association combines within-state changes, between-state differences, and time trends. The chapter’s panel design addresses a more specific comparison.')
practice('deaths_clean','Rebuild selected from dtype == "MVA" and repeat the state trend chart; keep its cause label accurate.',
 'Plot the unweighted yearly mean of all-cause state death rates and explain what receives equal weight.', 'Start with allcause, not the table containing all causes together.', 'Use allcause.groupby("year", as_index=False)["mrate"].mean().',
 '''yearly = allcause.groupby("year", as_index=False)["mrate"].mean()
fig = px.line(yearly, x="year", y="mrate", markers=True, labels=labels, title="Yearly mean: every available state has equal weight")
fig.show()''','The mean gives each state row equal weight, not each person. A population-weighted rate answers a different descriptive question.')
step('qob_clean','The familiar schooling gradient','How do average log wages vary with schooling?',
 'We summarize the full file by completed years of schooling. lnw is a natural logarithm: differences are on a proportional scale, not dollar differences. We do not exponentiate mean logs and call that mean earnings.',
 '''school = df.groupby("s", as_index=False).agg(lnw=("lnw", "mean"), people=("lnw", "count"))
fig = px.scatter(school, x="s", y="lnw", size="people", hover_data=["people"], labels=labels, title="Schooling and wages in the census extract")''',
 'Hover over common schooling levels. A larger circle means more available records, not a larger causal effect.',
 'The upward association includes the effects of selection into schooling. Grouping makes the pattern readable but does not remove confounding.')
step('qob_clean','Compare birthdays within a cohort','Are birth-quarter schooling differences visible within birth years?',
 'Grouping on both birth year and quarter produces one average for each combination. Keeping cohorts separate avoids attributing broad cohort differences to birth quarter.',
 '''cohorts = df.groupby(["yob", "qob"], as_index=False)[["s", "lnw"]].mean()
cohorts["birth_year"] = 1900 + cohorts["yob"]
cohorts["quarter"] = "Q" + cohorts["qob"].astype(str)
fig = px.line(cohorts, x="birth_year", y="s", color="quarter", markers=True, labels={"birth_year": "Birth year", "s": "Mean years of schooling", "quarter": "Birth quarter"}, title="Small schooling differences within cohorts")''',
 'Toggle Q2 and Q3 off to compare Q1 and Q4. Use hover to read differences that the axis may magnify.',
 'A small schooling difference may motivate an instrument, but small differences also demand careful inference. Birth timing is not automatically random with respect to every earnings determinant.')
step('qob_clean','Follow the link to earnings','Do the same quarter patterns appear in average log wages?',
 'We reuse the same cohort-quarter table and change the outcome. This keeps the groups comparable while asking a new question.',
 '''fig = px.line(cohorts, x="birth_year", y="lnw", color="quarter", markers=True, labels={"birth_year": "Birth year", "lnw": "Mean log weekly earnings", "quarter": "Birth quarter"}, title="The outcome link is a separate question")''',
 'Look at both the common cohort pattern and the within-cohort quarter differences. Which variation is larger?',
 'The instrument argument requires a connection to schooling and a reason to rule out other routes from birth timing to earnings. These charts establish neither assumption by themselves.')
practice('qob_clean','Change the outcome in the first summary to median log wages using median instead of mean.',
 'For men born in 1930 (yob == 30), plot mean schooling by quarter of birth.', 'Filter first so a birth-quarter comparison is made inside one cohort.', 'Then group by qob and average s.',
 '''cohort = df[df["yob"] == 30].groupby("qob", as_index=False)["s"].mean()
fig = px.bar(cohort, x="qob", y="s", labels=labels, title="Birth quarter within the 1930 cohort")
fig.show()''','Read the numerical size of the difference and the bar baseline. A birthday pattern is motivation for investigating assumptions, not proof of an education effect.')
step('twins_clean','Start with the individual pattern','Do more-schooled twins tend to have higher wages?',
 'Each dot is one stored individual. Discrete years of schooling produce vertical stacks; transparency helps reveal overlap. Wages are on a logarithmic scale.',
 '''fig = px.scatter(df, x="educ", y="lwage", opacity=0.5, labels=labels, title="Individuals: schooling and log wages")''',
 'Hover over observations at the same schooling level. How much variation remains?',
 'The individual association can reflect both schooling and background. A family comparison changes what variation we use.')
step('twins_clean','Switch to within-pair differences','When one twin has more schooling, does that twin also have higher wages?',
 'The chapter uses first == 1 to include supplied differences once per pair. Zero means the twins have the same reported schooling or log wage. The origin is the natural reference point.',
 '''pairs = df[df["first"] == 1].copy()
fig = px.scatter(pairs, x="deduc", y="dlwage", opacity=0.6, labels=labels, title="Within pairs: compare differences")
fig.add_hline(y=0, line_dash="dot")
fig.add_vline(x=0, line_dash="dot")''',
 'Find points with zero schooling difference but nonzero wage difference. What does that tell you?',
 'Twins can differ in earnings even when schooling matches. Shared background is only one set of influences, and pair differences can contain measurement error.')
step('twins_clean','Inspect the measurement itself','Do own-reported and twin-reported schooling differences agree?',
 'A point on a 45-degree diagonal would represent agreement between the two reports. Both axes measure a schooling difference in years.',
 '''fig = px.scatter(pairs, x="deduc", y="deduct", opacity=0.6, labels=labels, title="Two reports of the same schooling difference")
limits = [min(pairs["deduc"].min(), pairs["deduct"].min()), max(pairs["deduc"].max(), pairs["deduct"].max())]
fig.add_shape(type="line", x0=limits[0], y0=limits[0], x1=limits[1], y1=limits[1], line=dict(dash="dash", color="#7c3aed"))''',
 'Hover away from the agreement line. Could differences in reporting be large relative to differences in schooling?',
 'Disagreement makes measurement error a concrete concern. It does not reveal which report is correct or establish independence of the errors.')
practice('twins_clean','Restrict the pair scatter to deduc between −4 and 4. State that this is a restricted view, not the full sample.',
 'Make a histogram of within-pair schooling differences using one record per pair.', 'Use pairs, not df.', 'px.histogram(pairs, x="deduc") displays the distribution of differences.',
 '''fig = px.histogram(pairs, x="deduc", labels=labels, title="How much within-pair schooling variation is available?")
fig.show()''','If many pairs have similar schooling, identifying an effect relies on a smaller portion of the sample. Measurement error can then be especially consequential.')
step('childlabor_clean','Follow generations','How does average schooling vary across birth cohorts in these cells?',
 'We group by birth year and average the cell means. This gives each available cell equal weight; it is not a population-weighted estimate. The census waves can cover different cohorts.',
 '''cohorts = df.groupby(["yob", "year"], as_index=False)["indEduc"].mean()
cohorts["census"] = cohorts["year"].astype(str)
fig = px.line(cohorts, x="yob", y="indEduc", color="census", markers=True, labels={"yob": "Birth year", "indEduc": "Mean schooling across cells (years)", "census": "Census year"}, title="Schooling across cohorts: equal cell weights")''',
 'Toggle census years to compare the covered cohorts. Do not mistake the census year for a birth year.',
 'Cohort changes can reflect many historical developments. They cannot be attributed solely to schooling laws.')
step('childlabor_clean','Compare the law categories','Do cells in different requirement categories have similar schooling?',
 'The indicators classify child-labor schooling requirements. Rows with none of the three indicators form the reference category. We keep that label general because its precise composition requires the source coding.',
 '''laws = df.copy()
laws["requirement"] = "Reference category"
laws.loc[laws["cl7"] == 1, "requirement"] = "7 years"
laws.loc[laws["cl8"] == 1, "requirement"] = "8 years"
laws.loc[laws["cl9"] == 1, "requirement"] = "9+ years"
fig = px.box(laws, x="requirement", y="indEduc", color="requirement", points=False, labels={"requirement": "Required-schooling category", "indEduc": "Cell mean schooling (years)"}, title="Compare schooling across law categories")''',
 'Hover over the medians. What differences in state or cohort could accompany these law categories?',
 'The box plots mix states and cohorts. A relationship between laws and schooling is one part of an instrument argument, not proof that laws affect wages only through schooling.')
step('childlabor_clean','Put schooling and wages together','What does the schooling–wage pattern look like at the cell level?',
 'Each dot represents a cell, not a person. Color distinguishes census years, which may reveal why pooling them hides important differences.',
 '''cells = df.assign(census=df["year"].astype(str))
fig = px.scatter(cells, x="indEduc", y="lnwkwage", color="census", hover_data=["sob", "yob"], opacity=0.5, labels=labels, title="Cell averages mix education, place, and time")''',
 'Toggle census years. Describe whether the broad relationship changes within a wave.',
 'An aggregate association need not equal an individual return to schooling. Place, cohort, and census-year differences remain part of the comparison.')
practice('childlabor_clean','In the cohort line chart, replace schooling with lnwkwage and relabel the outcome as mean log weekly wages.',
 'Count how many cells are available in each required-schooling category and plot the counts.', 'Use laws, which contains the readable requirement category.', 'value_counts on requirement gives a count of cells, not a count of people.',
 '''counts = laws["requirement"].value_counts().rename_axis("requirement").reset_index(name="cells")
fig = px.bar(counts, x="requirement", y="cells", labels={"requirement": "Requirement category", "cells": "Stored cells"})
fig.show()''','Unequal numbers of cells remind us that an unweighted category comparison may represent different sets of cohorts and states.')
step('sheepskin_clean','First, check the credential link','Does passing coincide with a change in diploma receipt?',
 'receivehsd is a proportion; multiplying by 100 gives a percentage. We mark zero on the centered exam-score axis. Each point is a score-bin average.',
 '''scores = df.copy()
scores["diploma_percent"] = 100 * scores["receivehsd"]
fig = px.scatter(scores, x="minscore", y="diploma_percent", hover_data=["n"], labels={"minscore": "Score relative to passing threshold", "diploma_percent": "Received diploma (%)", "n": "Students in bin"}, title="Passing and receiving a diploma are different")
fig.add_vline(x=0, line_dash="dash")''',
 'Hover just to either side of zero. Notice whether every passing student receives a diploma.',
 'An imperfect link means the threshold changes the probability of a credential. It does not assign the credential perfectly.')
step('sheepskin_clean','Then, inspect later earnings','Is the earnings pattern equally discontinuous?',
 'We change the outcome while keeping the same score axis. These are mean earnings in years 7–11 from the source’s unbalanced panel, not starting salaries.',
 '''fig = px.scatter(df, x="minscore", y="avgearnings", hover_data=["n", "person_years"], labels=labels, title="Earnings around the same threshold")
fig.add_vline(x=0, line_dash="dash")''',
 'Compare this pattern with diploma receipt. Do not infer that a noisy or subtle pattern proves there is no effect.',
 'A credential jump and an earnings jump are separate pieces of evidence. Precision and the assumptions of the cutoff design matter.')
step('sheepskin_clean','Ask how much evidence supports a point','Are score bins equally informative?',
 'A bar chart of n reveals the number of students behind each score bin. The earnings denominator person_years is a different quantity.',
 '''fig = px.bar(df, x="minscore", y="n", labels=labels, title="Unequal numbers of students behind the averages")
fig.add_vline(x=0, line_dash="dash")''',
 'Compare sparse bins with the earnings chart. Which averages might be especially noisy?',
 'Treating every bin equally is not the same as treating every student equally. Weight choice must match the outcome and its denominator.')
practice('sheepskin_clean','Restrict the earnings chart to scores within 10 points of the threshold and state the restriction.',
 'Create a scatter plot of earnings near the cutoff with marker size representing students per bin.', 'Filter minscore using between(-10, 10).', 'Pass size="n" to px.scatter and keep person_years in hover_data.',
 '''near = df[df["minscore"].between(-10, 10)]
fig = px.scatter(near, x="minscore", y="avgearnings", size="n", hover_data=["person_years"], labels=labels)
fig.add_vline(x=0, line_dash="dash")
fig.show()''','Marker size communicates available information; it does not itself apply statistical weighting or measure uncertainty.')
step('synthetic_ovb','See the tempting association','Do simulated people with more schooling earn more?',
 'The generated earnings column is on a logarithmic scale. Transparency reveals overlapping observations at discrete schooling levels.',
 '''fig = px.scatter(df, x="schooling", y="earnings", opacity=0.4, labels=labels, title="A pattern that needs an explanation")''',
 'Inspect variation among people with the same schooling. A strong overall pattern still leaves individual differences.',
 'The association includes both schooling pathways and ability-related selection. The generator gives us a way to examine those components conceptually.')
step('synthetic_ovb','Reveal the common influence','Where do higher-ability people sit in the same chart?',
 'Color now represents a continuous ability score. A common influence on both axes can create or steepen an association.',
 '''fig = px.scatter(df, x="schooling", y="earnings", color="ability", opacity=0.6, labels=labels, title="Ability is related to both axes")''',
 'Hover over different color regions. Does ability appear related to schooling, earnings, or both?',
 'This is the visual signature of the confounding built into the simulation. Coloring points reveals a relationship; it does not statistically remove it.')
step('synthetic_ovb','A consequence is a different kind of variable','How does occupation vary with schooling?',
 'Occupation is generated partly from schooling. We average its coded status level by schooling to see this downstream relationship.',
 '''jobs = df.groupby("schooling", as_index=False)["occupation"].mean()
fig = px.line(jobs, x="schooling", y="occupation", markers=True, labels=labels, title="Schooling also changes a pathway to earnings")''',
 'Follow the line from low to high schooling. Why is occupation different from pre-existing ability?',
 'Holding a mediator fixed can remove part of a total effect. The right adjustment depends on the causal question, not simply on adding more columns.')
practice('synthetic_ovb','Change the color variable in the earnings scatter from ability to occupation. Explain why the causal role of color has changed.',
 'Plot mean log earnings by schooling separately for people above and below the median ability score.', 'Create an ability_group column using a comparison with the median.', 'Group by both schooling and ability_group, then draw colored lines.',
 '''groups = df.copy()
groups["ability_group"] = (groups["ability"] >= groups["ability"].median()).map({True: "Higher ability", False: "Lower ability"})
means = groups.groupby(["schooling", "ability_group"], as_index=False)["earnings"].mean()
fig = px.line(means, x="schooling", y="earnings", color="ability_group", markers=True, labels=labels)
fig.show()''','The broad ability split helps visualize confounding but does not fully hold continuous ability constant. It is not a controlled causal estimate.')
step('synthetic_rct','Start before the offer can matter','Are ability distributions similar across scholarship groups?',
 'A box plot compares a pre-existing characteristic across the randomized groups. Randomization balances distributions in expectation, not exactly in every finite sample.',
 '''offers = df.copy()
offers["offer"] = offers["scholarship"].map({0: "No scholarship", 1: "Scholarship offered"})
fig = px.box(offers, x="offer", y="ability", color="offer", points=False, labels=labels, title="Check a pre-existing characteristic")''',
 'Compare both the medians and the spread. Small differences can arise by chance.',
 'The generator assigns offers independently of ability. That independence comes from the assignment mechanism, not from a box plot proving equality.')
step('synthetic_rct','Did the offer change schooling?','How do schooling distributions differ between lottery groups?',
 'histnorm="percent" makes each group’s histogram sum to 100%. Overlaying transparent histograms helps compare the location and spread of schooling.',
 '''fig = px.histogram(offers, x="schooling", color="offer", histnorm="percent", barmode="overlay", opacity=0.55, labels=labels, title="An offer changes schooling, not by the same amount for everyone")''',
 'Toggle the groups and compare their centers. Notice overlapping schooling values.',
 'Scholarship assignment and schooling received are different variables. The distributional shift motivates a first-stage question in the chapter.')
step('synthetic_rct','Follow through to the outcome','Do mean log earnings differ across assignment groups?',
 'This is a comparison by randomized offer. It is not a comparison of people who chose the same number of school years.',
 '''means = offers.groupby("offer", as_index=False)["earnings"].mean()
fig = px.bar(means, x="offer", y="earnings", color="offer", labels=labels, title="The outcome comparison is by offer")''',
 'Hover to read the difference on the log scale. Explain why it is not a dollar amount or a per-year schooling effect.',
 'An offer effect can differ from an effect of education. Linking them requires assumptions about how the offer affects earnings.')
practice('synthetic_rct','Replace mean with median in the outcome comparison. Do the groups retain the same ordering?',
 'Plot the average years of schooling in the two assignment groups.', 'Use offers and group by offer.', 'Average schooling, then use px.bar with an accurate y-axis label.',
 '''means = offers.groupby("offer", as_index=False)["schooling"].mean()
fig = px.bar(means, x="offer", y="schooling", color="offer", labels=labels)
fig.show()''','A mean difference in schooling shows that the assignment changes the treatment received on average. It is not itself the effect of schooling on earnings.')
step('synthetic_did','Look at the full trajectory','Do the state groups start at the same level and move in the same direction?',
 'We average equally across states within each year and treatment group. The vertical guide marks the reform year, 2005.',
 '''trends = df.groupby(["year", "treated"], as_index=False)[["avg_schooling", "avg_earnings"]].mean()
trends["group"] = trends["treated"].map({0: "Comparison states", 1: "Reform states"})
fig = px.line(trends, x="year", y="avg_earnings", color="group", markers=True, labels=labels, title="Levels differ before the reform")
fig.add_vline(x=2005, line_dash="dash")''',
 'Compare the pre-2005 slopes separately from the levels. Hover to inspect the reform year.',
 'Parallel movement does not require equal levels. In this simulation the shared trend is imposed by the generator; real evidence cannot establish future parallel trends with certainty.')
step('synthetic_did','Follow the schooling mechanism','Does the schooling outcome shift at the same time?',
 'Reuse the same group-year table and change the outcome. This helps keep the comparison consistent across outcomes.',
 '''fig = px.line(trends, x="year", y="avg_schooling", color="group", markers=True, labels=labels, title="The reform and years of schooling")
fig.add_vline(x=2005, line_dash="dash")''',
 'Toggle the comparison group off and on. What would a before/after reading miss without it?',
 'Schooling was rising before the reform in both groups. The comparison trajectory helps us ask how much change would have occurred anyway.')
step('synthetic_did','Compare changes from a common reference','What happens when both paths start at zero in 2004?',
 'Subtract each group’s 2004 log-earnings mean from its full trajectory. Zero now means no change from that group’s own baseline.',
 '''base = trends[trends["year"] == 2004].set_index("group")["avg_earnings"]
trends["change"] = trends["avg_earnings"] - trends["group"].map(base)
fig = px.line(trends, x="year", y="change", color="group", markers=True, labels={"year": "Year", "change": "Change in mean log earnings since 2004", "group": "State group"}, title="A common baseline makes divergence visible")
fig.add_vline(x=2005, line_dash="dash")''',
 'Compare the post-reform separation with pre-reform variation. Do not confuse log points with dollars.',
 'The relative change is suggestive because the generator imposes the needed counterfactual trend. For real reforms, other group-specific shocks could produce the same picture.')
practice('synthetic_did','Change the normalization year from 2004 to 2000 and explain what changes and what does not.',
 'Plot individual schooling trajectories for reform states 1, 2, and 3.', 'Filter state with isin([1, 2, 3]) and sort by year.', 'Convert state to a string label so Plotly draws a separate line for each state.',
 '''states = df[df["state"].isin([1, 2, 3])].sort_values("year").copy()
states["state_name"] = states["state"].astype(str)
fig = px.line(states, x="year", y="avg_schooling", color="state_name", markers=True, labels=labels)
fig.add_vline(x=2005, line_dash="dash")
fig.show()''','Group averages hide state-specific noise. An individual state can wiggle around the common pattern without contradicting the simulation’s underlying trend.')

# Meanings are based on preparation code, Stata variable labels, and chapter usage.
DEFINITIONS = {
 'health':'Self-reported health score: 1 poor, 2 fair, 3 good, 4 very good, 5 excellent.',
 'insurance':'Insurance coverage indicator: 1 insured, 0 uninsured.',
 'nonwhite':'Source racial/ethnic indicator; NHIS nonwhite, RAND Black or Hispanic. It is not a biological measure.',
 'age':'Age in years.', 'education':'Years of education.', 'family_size':'Number of family members.',
 'employed':'Employment indicator: 1 employed, 0 otherwise.',
 'family_income':'Family income in source dollars; NHIS is constructed from income categories, RAND baseline uses source inflation-adjusted income.',
 'gender':'Husband/wife label constructed for this married-adult extract; not a general gender classification.',
 'weight':'Source person survey weight for NHIS; sample-line analysis weight for child-labor cells. Not a count of stored rows.',
 'female':'Source female indicator: 1 female, 0 otherwise.', 'white':'Source white indicator: 1 white, 0 otherwise.',
 'health_index':'Source general health index; higher values indicate better reported health. Distinct from the NHIS 1–5 score.',
 'cholesterol':'Source blood cholesterol measurement. Clinical unit is not independently documented in this CSV; do not infer it from the numeric scale.',
 'blood_pressure':'Source systolic blood pressure measurement. Clinical unit is not independently documented in this CSV.',
 'mental_health':'Source mental health index. Its exact scale is not independently documented in this CSV.',
 'plan_type':'Assigned plan: 1 free care, 2 deductible, 3 coinsurance, 4 catastrophic coverage. Missing means unknown.',
 'plan_free':'Indicator for the free-care plan; can be missing when plan is unknown.',
 'plan_deductible':'Indicator for the deductible plan. Inspect plan_type before interpreting zero.',
 'plan_coinsurance':'Indicator for the coinsurance plan. Inspect plan_type before interpreting zero.',
 'any_insurance':'Teaching indicator for plan types 1–3, not insurance versus no insurance; plan 4 also provides coverage. Preparation code maps unknown plans to 0.',
 'family_id':'Numeric family identifier constructed from source text. A grouping key, not a measured quantity.',
 'visits':'Number of face-to-face medical visits in a participant-year.',
 'outpatient_expenses':'Outpatient expenditure in constant 1991 dollars.', 'inpatient_expenses':'Inpatient expenditure in constant 1991 dollars.',
 'admissions':'Number of hospital admissions in a participant-year.', 'total_expenses':'Outpatient plus inpatient expenditure in constant 1991 dollars.',
 'assigned':'Police response assigned by the experiment: Arrest, Advise, or Separate.',
 'delivered':'Police response actually delivered; compare its category label with assigned.',
 'agecell':'Actual age in years for an aggregate mortality cell.', 'over21':'Indicator for the age-21 cutoff side: 1 at or above the threshold.',
 'all':'All-cause mortality rate, deaths per 100,000 person-years.', 'mva':'Motor-vehicle mortality rate, deaths per 100,000 person-years.',
 'suicide':'Suicide mortality rate, deaths per 100,000 person-years.', 'homicide':'Homicide mortality rate, deaths per 100,000 person-years.',
 'internal':'Mortality from internal causes, deaths per 100,000 person-years.', 'alcohol':'Alcohol-related mortality rate, deaths per 100,000 person-years.',
 'ext_oth':'Other external mortality, constructed by subtraction; deaths per 100,000 person-years.',
 'age2':'Squared age term; uses centered age in the drinking-age file and actual age in the twins file.',
 'over_age':'Interaction: over21 × centered age.', 'over_age2':'Interaction: over21 × squared centered age.',
 'year':'Calendar year of the observation; census year in the child-labor file.',
 'bib6':'Number of banks in business in the sixth Federal Reserve district on the July 1 snapshot.',
 'bib8':'Number of banks in business in the eighth Federal Reserve district on the July 1 snapshot.',
 'counterfactual':'Constructed sixth-district path holding the 1930 sixth–eighth district gap fixed; not observed.',
 'state':'State identifier. Empirical state-panel codes follow U.S. state coding; simulated state IDs have no real geography.',
 'dtype':'Cause of death: all (all causes), MVA (motor vehicles), suicide, or internal. Filter before averaging rates.',
 'mrate':'Mortality rate per 100,000 in the chapter’s ages 18–20 population.',
 'legal':'Share of the relevant age group legally allowed to drink, from 0 to 1.',
 'pop':'Population of the relevant state-year age group; chapter uses this as a population analysis weight.',
 'beertax':'Source beer-tax measure; currency/base-year details are not independently documented in this extract.',
 'lnw':'Natural logarithm of weekly earnings; not dollar earnings.', 's':'Completed years of schooling.',
 'qob':'Quarter of birth: 1 January–March through 4 October–December.', 'yob':'Year of birth; two-digit 1930s codes in qob_clean, full years in childlabor_clean.',
 'q1':'Indicator for birth in quarter 1.', 'q2':'Indicator for birth in quarter 2.', 'q3':'Indicator for birth in quarter 3.', 'q4':'Indicator for birth in quarter 4.',
 'lwage':'Natural logarithm of wage in the twins source; not a dollar wage.', 'educ':'Own-reported years of education.',
 'educt_t':'Twin-reported education of the respondent, in years.', 'first':'Indicator selecting the first record per twin pair; use 1 for supplied pair differences.',
 'dlwage':'Supplied within-pair difference in log wages.', 'deduc':'Supplied within-pair difference in own-reported years of education.',
 'deduct':'Supplied within-pair difference in twin-reported years of education.',
 'sob':'State of birth identifier.', 'lnwkwage':'Cell mean of log weekly wages.', 'indEduc':'Cell mean of highest completed grade (years).',
 'cl7':'Indicator for child-labor required-schooling category of 7 years; not entry age.',
 'cl8':'Indicator for child-labor required-schooling category of 8 years; not entry age.',
 'cl9':'Indicator for child-labor required-schooling category of at least 9 years; not entry age.',
 'n':'Stored cell count in childlabor_clean; number of students in the score bin in sheepskin_clean.',
 'minscore':'Last-chance exam score relative to the passing threshold (0).', 'pass_exam':'Indicator for passing the exam threshold.',
 'receivehsd':'Proportion receiving a high-school diploma in the score bin, from 0 to 1.',
 'avgearnings':'Score-bin mean earnings in years 7–11, computed on the source unbalanced panel; source dollars.',
 'person_years':'Person-year observations supporting the earnings outcome in a score bin; not interchangeable with student count n.',
 'schooling':'Simulated completed years of schooling, clipped to 6–20 and rounded.',
 'earnings':'Simulated log earnings; the column name does not indicate dollars.',
 'ability':'Simulated pre-existing ability score (standard normal in Chapter 6).',
 'occupation':'Simulated occupation-status category 1–5, partly caused by schooling; a mediator.',
 'scholarship':'Randomized simulated scholarship offer: 1 offered, 0 not offered.',
 'treated':'Indicator for simulated reform states 1–10 (1), versus comparison states 11–20 (0).',
 'post':'Indicator for simulated years 2005 onward.',
 'avg_schooling':'Simulated state-year average years of schooling.', 'avg_earnings':'Simulated state-year average log earnings, not dollars.',
}
for side in ['left','right']:
 for power in range(1,5):
  DEFINITIONS[f'{side}_{power}']=f'Source polynomial term of order {power} on the {side} side of the exam cutoff; used in the chapter regression.'
LABELS = {
 'plan':'Assigned insurance plan','age':'Age (years)','education':'Education (years)',
 'health_index':'General health index (source scale)','blood_pressure':'Systolic blood pressure (source units)',
 'cholesterol':'Cholesterol (source units)','visits':'Visits per participant-year','total_expenses':'Annual expenses (1991 dollars)',
 'admissions':'Admissions per participant-year','agecell':'Age (years)','all':'Deaths per 100,000 person-years',
 'mva':'Motor-vehicle deaths per 100,000 person-years','mrate':'Deaths per 100,000 (ages 18–20)',
 'legal':'Share legally allowed to drink','year':'Year','state':'State code',
 's':'Years of schooling','lnw':'Mean log weekly earnings','qob':'Quarter of birth',
 'educ':'Own-reported schooling (years)','lwage':'Log wage','deduc':'Own-reported schooling difference (years)',
 'deduct':'Twin-reported schooling difference (years)','dlwage':'Within-pair log-wage difference',
 'indEduc':'Cell mean schooling (years)','lnwkwage':'Cell mean log weekly wages','sob':'Birth-state code','yob':'Birth year','census':'Census year',
 'minscore':'Score relative to passing threshold','n':'Students in score bin','avgearnings':'Mean earnings, years 7–11 (source dollars)',
 'person_years':'Earnings person-years','schooling':'Years of schooling','earnings':'Log earnings','ability':'Simulated ability score',
 'occupation':'Occupation status (1–5)','offer':'Scholarship assignment','avg_schooling':'Mean years of schooling',
 'avg_earnings':'Mean log earnings','group':'State group','state_name':'Simulated state','ability_group':'Ability group',
}

PREP = {
 'rand_balance':'plans = df[df["plan_type"].notna()].copy()\nplans["plan"] = plans["plan_type"].map({1: "Free care", 2: "Deductible", 3: "Coinsurance", 4: "Catastrophic"})',
}
PREP['rand_utilization']=PREP['rand_balance']
PREP['rand_health_outcomes']=PREP['rand_balance']

# Outcome/group/weight triples are documented in the chapter or preparation code.
WEIGHTS = {
 'nhis_clean': ('health','insurance','weight','Person survey weights give more influence to respondents representing more people. This remains a descriptive comparison of the selected extract, not a survey-design variance estimate.'),
 'deaths_clean': ('mrate','year','pop','First restrict to all-cause mortality. Population weighting gives larger age-group populations more influence; it answers a different question from an equal-state mean.'),
 'childlabor_clean': ('indEduc','year','weight','The chapter uses the source sample-line weight. Compare weighted and equal-cell schooling summaries within a census year; neither comparison identifies a law effect.'),
 'sheepskin_clean': ('receivehsd','pass_exam','n','Weight diploma proportions by the student count n. Do not reuse this weight uncritically for earnings, whose source denominator is person_years. A whole-side average is not a local cutoff estimate.'),
}

# Verified section IDs in the tracked, published Quarto book.
GUIDE_ANCHORS = {
 'nhis_clean':'does-health-insurance-improve-health',
 'rand_balance':'step-1-verify-randomization-balance-check',
 'rand_utilization':'step-2-estimate-causal-effects-on-health-care-use',
 'rand_health_outcomes':'step-3-estimate-causal-effects-on-health',
 'mdve_clean':'the-minneapolis-domestic-violence-experiment',
 'mlda_clean':'the-mlda-question',
 'banks_clean':'a-mississippi-experiment',
 'deaths_clean':'case-study-mlda-and-death-rates',
 'qob_clean':'strategy-2-quarter-of-birth-iv',
 'twins_clean':'strategy-1-twin-comparisons',
 'childlabor_clean':'strategy-3-child-labor-law-iv',
 'sheepskin_clean':'strategy-4-sheepskin-effects-via-rd',
 'synthetic_ovb':'seeing-ovb-in-action',
 'synthetic_rct':'why-not-an-rct',
 'synthetic_did':'strategy-5-differences-in-differences',
}
