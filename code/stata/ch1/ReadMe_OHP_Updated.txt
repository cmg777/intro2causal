** ReadMe_OHP.txt **

This folder contains links to the data and programs used to generate Tables 1.5
and 1.6 in Mastering Metrics. Table 1.5 presents estimates of the
effects of winning the Oregon Health Plan (OHP) lottery on insurance
coverage and health care utilization. Table 1.6 presents estimates of
the effects of winning the OHP lottery on health indicators and
financial health. Data and programs are available at The Oregon Health Insurance Experiment website (http://www.nber.org/oregon/4.data.html). In order to access the data and code, you will need to use an NBER login. If you do not have one, you can create an account for free at https://www.nber.org/login/.

Source notes: 
Tables 1.5 is derived from:
* Finkelstein et al., "The Oregon Health Insurance Experiment: Evidence from the First Year,"
QJE (2012) 
- Table III (Panel A, Columns 1 and 2 of Table 1.5)
- Table IV, Panel A (Panel A, Columns 1 and 2 of Table 1.5)
- Table V (Panel B, Columns 1 and 2 of Table 1.5)
* Taubman et al., "Medicaid Increases Emergency Department Use: Evidence
from Oregon's Health Insurance Experiment," Science (2014) 
- Table S2 (Panel A, Columns 3 and 4 of Table 1.5)
- Table S7 (Panel A, Columns 3 and 4 of Table 1.5)

Tables 1.6 is derived from:
* Finkelstein et al., "The Oregon Health Insurance Experiment: Evidence from the First Year,"
QJE (2012) 
- Table IX (Columns 1 and 2 of Table 1.6)
* Baicker et al., "The Oregon Experiment -- Effects of Medicaid on
Clinical Outcomes," NEJM (2013) 
- Table S1 (Columns 3 and 4 of Table 1.6)
- Table S2 (Columns 3 and 4 of Table 1.6)
- Table S3 (Columns 3 and 4 of Table 1.6)
- Note that standard errors in column (4) of Table 1.6 are calculated manually using point estimates and confidence intervals from Baicker et al. (2013). 



Code: 
Main programs:
* oregon_hie_qje_replication.do
	- This program replicates Tables III, V, and IX of the QJE paper. Table IV cannot be replicated because the required data is not publicly available. 
* oregon_hie_nejm_replication.do
	- This program replicates Tables S1, S2, and S3 from the NEJM paper.
* oregonhie_science_replication.do
	- This program replicates Table S7 and parts of Table S2 from the Science paper. Other parts of Table S2 cannot be replicated because the required data is not publicly available.

Additional programs are contained in folders named Programs_QJE, Programs_NEJM, and Programs_Science. These programs are called by the main programs above. 


Data: 
* Download the Oregon Health Insurance Experiment Public Use Data from http://www.nber.org/oregon/data.html. The required data files are:
- oregonhie_descriptive_vars.dta
- oregonhie_ed_vars.dta
- oregonhie_inperson_vars.dta
- oregonhie_stateprograms_vars.dta
- oregonhie_survey0m_vars.dta
- oregonhie_survey6m_vars.dta
- oregonhie_survey12m_vars.dta
* After downloading the above data files, save them in a folder titled "Data" and save the "Data" folder in the same directory as your .do files.

Output:
* all_tables_qje.log (output for Tables III, V, and IX of QJE paper)
* paper_tables_nejm.log (output for Tables S1, S2, and S3 of the NEJM paper)
* all_tables_science.log (output for Table S7 and parts of S2 of the Science paper)

