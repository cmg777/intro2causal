## JOSHUA D. ANGRIST \& JÖRN-STEFFEN PISCHKE

## MASTERING METRICS

## THE PATH FROM CAUSE TO EFFECT

## Mastering 'Metrics

# Mastering 'Metrics <br> The Path from Cause to Effect 

Joshua D. Angrist<br>and<br>Jörn-Steffen Pischke

Published by Princeton University Press, 41 William Street, Princeton, New Jersey 08540 In the United Kingdom: Princeton University Press, 6 Oxford Street, Woodstock, Oxfordshire OX20 1TW
press.princeton.edu
Jacket and illustration design by Wanda Espana
Book illustrations by Garrett Scafani
All Rights Reserved
Library of Congress Cataloging-in-Publication Data
Angrist, Joshua David.
Mastering 'metrics : the path from cause to effect / Joshua D. Angrist, Jörn-Steffen Pischke.
pages cm
Includes index.
Summary: "Applied econometrics, known to aficionados as 'metrics, is the original data science.
'Metrics encompasses the statistical methods economists use to untangle cause and effect in human affairs. Through accessible discussion and with a dose of kung fu-themed humor, Mastering 'Metrics presents the essential tools of econometric research and demonstrates why econometrics is exciting and useful. The five most valuable econometric methods, or what the
authors call the Furious Five-random assignment, regression, instrumental variables, regression discontinuity designs, and differences in differences-are illustrated through wellcrafted real-world examples (vetted for awesomeness by Kung Fu Panda's Jade Palace). Does health insurance make you healthier? Randomized experiments provide answers. Are expensive private colleges and selective public high schools better than more pedestrian institutions? Regression analysis and a regression discontinuity design reveal the surprising truth. When private banks teeter, and depositors take their money and run, should central banks step in to save them? Differences-indifferences analysis of a Depression-era banking crisis offers a response. Could arresting O.J. Simpson have saved his ex-wife's life? Instrumental variables methods instruct law enforcement authorities in how best to respond to domestic abuse. Wielding econometric tools with skill and confidence, Mastering 'Metrics uses data and statistics to illuminate the path from cause to effect.

Shows why econometrics is important Explains econometric research through humorous and accessible discussion Outlines empirical methods central to modern econometric practice Works through interesting and relevant real-world examples"-Provided by publisher.

ISBN 978-0-691-15283-7 (hardback : alk. paper)ISBN 978-0-691-15284-4 (paperback : alk. paper)

1. Econometrics. I. Pischke, Jörn-Steffen. II. Title.

HB139.A53984 2014
330.01'5195—dc23 2014024449

British Library Cataloging-in-Publication Data is available
This book has been composed in Sabon with Helvetica Neue Condensed family display using ZzTEX by Princeton Editorial Associates Inc., Scottsdale, Arizona

Printed on acid-free paper.
Printed in the United States of America
13579108642

## CONTENTS

List of Figures ..... vii
List of Tables ..... ix
Introduction ..... xi
1 Randomized Trials ..... 1
1.1 In Sickness and in Health (Insurance) ..... 1
1.2 The Oregon Trail ..... 24
Masters of 'Metrics: From Daniel to R. A. Fisher ..... 30
Appendix: Mastering Inference ..... 33
2 Regression ..... 47
2.1 A Tale of Two Colleges ..... 47
2.2 Make Me a Match, Run Me a Regression ..... 55
2.3 Ceteris Paribus? ..... 68
Masters of 'Metrics: Galton and Yule ..... 79
Appendix: Regression Theory ..... 82
3 Instrumental Variables ..... 98
3.1 The Charter Conundrum ..... 99
3.2 Abuse Busters ..... 115
3.3 The Population Bomb ..... 123
Masters of 'Metrics: The Remarkable Wrights ..... 139
Appendix: IV Theory ..... 142
4 Regression Discontinuity Designs ..... 147
4.1 Birthdays and Funerals ..... 148
4.2 The Elite Illusion ..... 164
Masters of 'Metrics: Donald Campbell ..... 175
5 Differences-in-Differences ..... 178
5.1 A Mississippi Experiment ..... 178
5.2 Drink, Drank, ..... 191
Masters of 'Metrics: John Snow ..... 204
Appendix: Standard Errors for Regression DD ..... 205
6 The Wages of Schooling ..... 209
6.1 Schooling, Experience, and Earnings ..... 209
6.2 Twins Double the Fun ..... 217
6.3 Econometricians Are Known by Their ... Instruments ..... 223
6.4 Rustling Sheepskin in the Lone Star State ..... 235
Appendix: Bias from Measurement Error ..... 240
Abbreviations and Acronyms ..... 245
Empirical Notes ..... 249
Acknowledgments ..... 269
Index ..... 271

## FIGURES

1.1 A standard normal distribution ..... 40
1.2 The distribution of the $t$-statistic for the mean in a sample ..... 41 of size 10
1.3 The distribution of the $t$-statistic for the mean in a sample ..... 42 of size 40
1.4 The distribution of the $t$-statistic for the mean in a sample ..... 42 of size 100
2.1 The CEF and the regression line ..... 83
2.2 Variance in $X$ is good ..... 96
3.1 Application and enrollment data from KIPP Lynn lotteries ..... 103
3.2 IV in school: the effect of KIPP attendance on math scores ..... 108
4.1 Birthdays and funerals ..... 149
4.2 A sharp RD estimate of MLDA mortality effects ..... 150
4.3 RD in action, three ways ..... 154
4.4 Quadratic control in an RD design ..... 158
4.5 RD estimates of MLDA effects on mortality by cause of ..... 161 death
4.6 Enrollment at BLS ..... 166
4.7 Enrollment at any Boston exam school ..... 167
4.8 Peer quality around the BLS cutoff ..... 168
4.9 Math scores around the BLS cutoff ..... 172
4.10 Thistlethwaite and Campbell's Visual RD ..... 177
5.1 Bank failures in the Sixth and Eighth Federal Reserve ..... 184 Districts
5.2 Trends in bank failures in the Sixth and Eighth Federal ..... 185
Reserve Districts
5.3 Trends in bank failures in the Sixth and Eighth Federal ..... 186 Reserve Districts, and the Sixth District's DD counterfactual
5.4 An MLDA effect in states with parallel trends ..... 198
5.5 A spurious MLDA effect in states where trends are not ..... 198 parallel
5.6 A real MLDA effect, visible even though trends are not ..... 199 parallel
5.7 John Snow’s DD recipe ..... 206
6.1 The quarter of birth first stage ..... 230
6.2 The quarter of birth reduced form ..... 230
6.3 Last-chance exam scores and Texas sheepskin ..... 237
6.4 The effect of last-chance exam scores on earnings ..... 237

## TABLES

1.1 Health and demographic characteristics of insured and ..... 5 uninsured couples in the NHIS
1.2 Outcomes and treatments for Khuzdar and Maria ..... 7
1.3 Demographic characteristics and baseline health in the ..... 20 RAND HIE
1.4 Health expenditure and health outcomes in the RAND HIE ..... 23
1.5 OHP effects on insurance coverage and health-care use ..... 27
1.6 OHP effects on health indicators and financial health ..... 28
2.1 The college matching matrix ..... 53
2.2 Private school effects: Barron's matches ..... 63
2.3 Private school effects: Average SAT score controls ..... 66
2.4 School selectivity effects: Average SAT score controls ..... 67
2.5 Private school effects: Omitted variables bias ..... 76
3.1 Analysis of KIPP lotteries ..... 104
3.2 The four types of children ..... 112
3.3 Assigned and delivered treatments in the MDVE ..... 117
3.4 Quantity-quality first stages ..... 135
3.5 OLS and 2SLS estimates of the quantity-quality trade-off ..... 137
4.1 Sharp RD estimates of MLDA effects on mortality ..... 160
5.1 Wholesale firm failures and sales in 1929 and 1933 ..... 190
5.2 Regression DD estimates of MLDA effects on death rates ..... 196
5.3 Regression DD estimates of MLDA effects controlling for ..... 201 beer taxes
6.1 How bad control creates selection bias ..... 216
6.2 Returns to schooling for Twinsburg twins ..... 220
6.3 Returns to schooling using child labor law instruments ..... 226
6.4 IV recipe for an estimate of the returns to schooling using ..... 231 a single quarter of birth instrument
6.5 Returns to schooling using alternative quarter of birth ..... 232 instruments

