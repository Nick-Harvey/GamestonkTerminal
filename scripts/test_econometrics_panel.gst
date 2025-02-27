econometrics
load wage_panel wp
options
options wp
show wp
index wp nr year
clean wp -f cfill
clean wp -d rdrop
type
type year-wp category
desc wp
modify -a dummy_married_educ-wp married-wp * educ-wp
modify -d married-wp
load wage_panel wp2
index wp2 nr year
modify -c wp married-wp2
modify -r wp married_wp2 married
remove wp2
panel lwage-wp black-wp hisp-wp exper-wp expersq-wp married-wp educ-wp union-wp year-wp
panel lwage-wp black-wp hisp-wp exper-wp married-wp educ-wp union-wp -t bols
panel lwage-wp black-wp hisp-wp exper-wp expersq-wp married-wp educ-wp union-wp year-wp -t re
panel lwage-wp expersq-wp union-wp married-wp  year-wp -t fe
panel lwage-wp expersq-wp union-wp married-wp  year-wp -t fe -ee
panel lwage-wp expersq-wp union-wp married-wp  -t fe -te
panel lwage-wp expersq-wp union-wp married-wp  -t fe -te -ee
panel lwage-wp exper-wp expersq-wp union-wp married-wp -t fdols
dwat -p
bgod
granger married-wp educ-wp
coint black-wp hisp-wp exper-wp expersq-wp married-wp educ-wp union-wp
